#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x,
                            5.86962678,
                            -0.88019874,
                            -0.00000000,
                            -0.01923988,
                            1.18619240,
                            0.00000000,
                            3.66533036,
                            -0.37157951,
                            1.82381363
                        ) + 5.77122153;
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
