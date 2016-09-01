prices <- read.csv('./prices(1).csv')



prices.ftest <- function (prices) {
  mp.prices <- prices[prices$Area == 'MP',-1]
  pa.prices <- prices[prices$Area == 'PA',-1]
  
  mu.pa <- as.matrix(sapply(pa.prices,mean))
  mu.mp <- as.matrix(sapply(mp.prices,mean))
  
  
  mp.prices <- as.matrix(mp.prices)
  
  pa.prices <- as.matrix(pa.prices)
  
  S1 <- cov(pa.prices)
  S2 <- cov(mp.prices)
  n1 <- dim(pa.prices)[1]
  n2 <- dim(mp.prices)[1]
  p = 4
  
  S <- (n1 - 1) * S1 + (n2 - 1) * S2 / (n1 + n2 - 2)
  
  D_sqrd = t(mu.pa - mu.mp) %*% solve(S) %*% (mu.pa - mu.mp)
  T_sqrd = ((n1 * n2) * D_sqrd) / (n1 + n2)
  
  F = ((n1 + n2 - p - 1) * T_sqrd) / ((n1 + n2 - 2) * p)
  
  F_crit = qf(.95, df1 = p, df2 = n1 + n2 - p - 1)
  
  if (F > F_crit)
    return ("reject null hypothesis for alpha = 0.05")
  else
    return (" accept null hypothesis for alpha = 0.05")
}
