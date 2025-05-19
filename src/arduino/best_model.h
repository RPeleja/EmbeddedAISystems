#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x, COEF_0, COEF_1, ..., COEF_N) + INTERCEPT;
                    }

                protected:
                    float dot(float *x, ...) {
                        va_list w;
                        va_start(w, 5); // Substituir por número de features
                        float dot = 0.0;
                        for (uint16_t i = 0; i < NUM_FEATURES; i++) {
                            const float wi = va_arg(w, double);
                            dot += x[i] * wi;
                        }
                        return dot;
                    }
            };
        }
    }
}
