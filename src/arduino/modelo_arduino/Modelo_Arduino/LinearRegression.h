#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x,
                            0.38659299,
                            -0.84765902,
                            -0.00000000,
                            0.02806151,
                            0.94627942,
                            0.00000000,
                            0.00000000,
                            0.02944015,
                            0.21587318
                        ) + 2.72852234;
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
