#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x,
                            3.06956014,
                            -4.32799341
                        ) + 5.77122153;
                    }

                protected:
                    float dot(float *x, ...) {
                        va_list w;
                        va_start(w, 2);
                        float dot = 0.0;
                        for (uint16_t i = 0; i < 2; i++) {
                            const float wi = va_arg(w, double);
                            dot += x[i] * wi;
                        }
                        return dot;
                    }
            };
        }
    }
}
