#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x,
                            0.97370080,
                            -0.09401285,
                            0.00000000,
                            -1.83825140,
                            -4.86000171,
                            0.00000000,
                            0.00000000,
                            0.11015398,
                            0.74087806
                        ) + -12.45504742;
                    }

                protected:
                    float dot(float *x, ...) {
                        va_list w;
                        va_start(w, 9);
                        float dot = 0.0;
                        for (uint16_t i = 0; i < 9; i++) {
                            const float wi = va_arg(w, double);
                            dot += x[i] * wi;
                        }
                        return dot;
                    }
            };
        }
    }
}
