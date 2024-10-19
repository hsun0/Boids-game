#include <cmath>
#include <vector>
#include <random>
#include <algorithm>

#ifdef _WIN32
#define DLL_EXPORT extern "C" __declspec(dllexport)
#else
#define DLL_EXPORT extern "C"
#endif

struct Vector2 {
    float x;
    float y;

    Vector2 operator+(const Vector2& other) const {
        return {x + other.x, y + other.y};
    }
    
    Vector2 operator-(const Vector2& other) const {
        return {x - other.x, y - other.y};
    }
    
    Vector2 operator*(float scalar) const {
        return {x * scalar, y * scalar};
    }
};

struct Boid {
    Vector2 pos;
    Vector2 vel;
    float energy;
    int color;
    float mass;
};

// 統一配置參數結構
struct SimulationParams {
    // 基本設定
    float vision_radius;
    float max_speed;
    float min_speed;
    
    // 行為因子
    float separation_factor;
    float alignment_factor;
    float cohesion_factor;
    float color_avoidance_factor;
    float energy_factor;
};

// 輔助函數
float vector_length(Vector2 v) {
    return std::sqrt(v.x * v.x + v.y * v.y);
}

Vector2 normalize(Vector2 v) {
    float len = vector_length(v);
    if (len > 0) {
        return {v.x / len, v.y / len};
    }
    return v;
}

// 計算環繞距離
Vector2 calculate_wrapped_distance(Vector2 pos1, Vector2 pos2, float width, float height) {
    Vector2 diff = pos1 - pos2;
    
    if (diff.x > width/2) diff.x -= width;
    else if (diff.x < -width/2) diff.x += width;
    
    if (diff.y > height/2) diff.y -= height;
    else if (diff.y < -height/2) diff.y += height;
    
    return diff;
}

DLL_EXPORT void update_boids(
    Boid* boids, int boid_count,
    float canvas_width, float canvas_height,
    const SimulationParams* params
) {
    #pragma omp parallel for
    for (int i = 0; i < boid_count; i++) {
        Vector2 separation = {0, 0};
        Vector2 alignment = {0, 0};
        Vector2 cohesion = {0, 0};
        Vector2 color_avoidance = {0, 0};
        Vector2 energy_direction = {0, 0};
        
        int same_color_count = 0;
        int different_color_count = 0;
        float total_nearby_energy = 0;

        // 計算與其他 boids 的互動
        for (int j = 0; j < boid_count; j++) {
            if (i == j) continue;

            Vector2 diff = calculate_wrapped_distance(
                boids[i].pos, boids[j].pos, 
                canvas_width, canvas_height
            );
            float dist = vector_length(diff);
            
            if (dist < params->vision_radius) {
                float weight = 1.0f / (dist + 1e-6f);
                
                if (boids[i].color == boids[j].color) {
                    same_color_count++;
                    
                    // 分離
                    if (dist < params->vision_radius * 0.3f) {
                        separation = separation + (diff * weight);
                    }
                    
                    // 對齊
                    alignment = alignment + boids[j].vel;
                    
                    // 凝聚
                    cohesion = cohesion + boids[j].pos;
                    
                    // 能量影響
                    if (boids[j].energy > boids[i].energy) {
                        energy_direction = energy_direction + diff * weight;
                        total_nearby_energy += boids[j].energy;
                    }
                } else {
                    different_color_count++;
                    color_avoidance = color_avoidance + (diff * weight * 2.0f);
                }
            }
        }

        // 應用群體規則
        Vector2 velocity_change = {0, 0};
        
        if (same_color_count > 0) {
            float inv_count = 1.0f / same_color_count;
            alignment = alignment * inv_count;
            cohesion = (cohesion * inv_count) - boids[i].pos;
            
            // 使用統一的參數
            velocity_change = velocity_change + (separation * params->separation_factor);
            velocity_change = velocity_change + (alignment * params->alignment_factor);
            velocity_change = velocity_change + (cohesion * params->cohesion_factor);
        }
        
        // 能量和顏色影響
        if (total_nearby_energy > 0) {
            velocity_change = velocity_change + (energy_direction * params->energy_factor);
        }
        velocity_change = velocity_change + (color_avoidance * params->color_avoidance_factor);

        // 根據質量調整速度變化
        velocity_change = velocity_change * (1.0f / boids[i].mass);

        // 更新速度
        boids[i].vel = boids[i].vel + velocity_change;

        // 限制速度
        float speed = vector_length(boids[i].vel);
        if (speed > params->max_speed) {
            boids[i].vel = normalize(boids[i].vel) * params->max_speed;
        } else if (speed < params->min_speed) {
            boids[i].vel = normalize(boids[i].vel) * params->min_speed;
        }

        // 更新位置
        boids[i].pos = boids[i].pos + boids[i].vel;
        
        // 處理環繞邊界
        boids[i].pos.x = fmod(boids[i].pos.x + canvas_width, canvas_width);
        boids[i].pos.y = fmod(boids[i].pos.y + canvas_height, canvas_height);
    }
}