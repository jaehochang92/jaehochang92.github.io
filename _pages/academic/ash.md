---
title: "Academic Works"
permalink: /academic/ash/
author_profile: true
---

ASH.cpp\
Don't forget to include `// [[Rcpp::export()]]`!
```cpp
# include <Rcpp.h>
using namespace Rcpp;
// [[Rcpp::export()]]

NumericVector Cfx (NumericVector x, NumericVector data, int K, int m) {
  int J = x.length(); 
  int n = data.length();
  double h = (max(data) - min(data)) / K;
  double eps = h;
  double c1, c2, c3, c4, c5;
  NumericVector ret(J);
  for (int j = 0; j < J; j++){
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
      for (int k = 1; k < (K * m); k++) {
        for (int l = (1 - m); l < (m - 1); l++) {
          c1 = 1 - std::fabs(l) / m;
          c2 = (k + l - 1) * h / m;
          c3 = (k + l) * h / m;
          c4 = (k - 1) * h / m;
          c5 = k * h / m;
          if (k == 1) {
            sum += c1 * (c4 - eps <= x(j) & x(j) < c5) * (c2 <= data(i) & data(i) < c3);
          } else if (k == K * m) {
            sum += c1 * (c4 <= x(j) & x(j) < c5) * (c2 <= data(i) & data(i) < c3 + eps);
          } else {
            sum += c1 * (c4 <= x(j) & x(j) < c5) * (c2 <= data(i) & data(i) < c3);
          }
        }
      }
    }
    ret(j) = sum;
  }
  return ret / (n * h);
}
```
>You can include R code blocks in C++ files processed with `sourceCpp`(useful for testing and development). The R code will be automatically  run after the compilation.

Main R code
```r
rm(list = ls())
require(ggplot2)
require(Rcpp)
sourceCpp('Rcpp/ASH.cpp')
`%+=%` = function(e1, e2)
  eval.parent(substitute(e1 <- e1 + e2))
set.seed(30)

n <-  300
M <- rmultinom(n, 1, c(.2, .5, .3))
data <-
  M[1,] * rnorm(n) + M[2,] * rnorm(n, 5) + M[3,] * rnorm(n, 10)
cat(range(data))
x <- sort(data + rnorm(n, 0, 0.01))
system.time(f <- Cfx(x, data = data, K = 20, m = 10))  # very fast!

df <- data.frame(x = x, data = sort(data), f = f)
ggplot(df) +
  geom_histogram(
    aes(x = data, y = ..density..),
    colour = "black",
    fill = "cadetblue3",
    stat = 'bin',
    binwidth = .5
  ) +
  geom_line(aes(x = x, y = f, lty = 'ASH'), lwd = 1.2, col = 'blue')
```

<img src='https://jaehochang92.github.io/images/ash.svg' width="700px">
