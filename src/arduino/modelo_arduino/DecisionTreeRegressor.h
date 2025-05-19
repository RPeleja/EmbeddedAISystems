double score(double * input) {
    double var0;
    if (input[1] <= -0.30409057438373566) {
        if (input[1] <= -1.1610096096992493) {
            if (input[1] <= -1.5918627381324768) {
                var0 = 28.695652173913043;
            } else {
                var0 = 23.75;
            }
        } else {
            if (input[1] <= -0.624836802482605) {
                var0 = 18.0;
            } else {
                var0 = 13.5;
            }
        }
    } else {
        if (input[0] <= 1.0685769021511078) {
            if (input[1] <= -0.0982385091483593) {
                var0 = 7.333333333333333;
            } else {
                var0 = 1.8803418803418803;
            }
        } else {
            if (input[0] <= 1.6712420582771301) {
                var0 = 11.0;
            } else {
                var0 = 13.0;
            }
        }
    }
    return var0;
}
