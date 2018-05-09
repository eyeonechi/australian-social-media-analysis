# CCC Team 42, Melbourne
# 
# Thuy Ngoc Ha - 963370
# Lan Zhou - 824371
# Zijian Wang - 950618			
# Ivan Chee - 736901
# Duer Wang - 824325

# R script that perform some basic correlation analysis

# read files
data_pos = read.csv("Desktop/90024/data/output_positive.csv")
data_neg = read.csv("Desktop/90024/data/output_negative.csv")
tdata = read.csv("Desktop/90024/data/output_polarity.csv")

# check correlation
cor(data_pos)
cor(data_neg)

x1 = data_pos[, 1]
y1 = data_pos[, 2]
z1 = data_pos[, 3]
x2 = data_neg[, 1]
y2 = data_neg[, 2]
z2 = data_neg[, 3]

# plot 

plot(x1, y1, main="Basic Scatterplot of Homeless vs. Positive Polarity",xlab="Polarity", ylab="Homeless", pch=19)
abline(lm(y1 ~ x1), col="red", lwd=2, lty=1)

plot(x1, z1, main="Basic Scatterplot of Homeless Trend vs. Positive Polarity",xlab="Polarity", ylab="Homeless Trend", pch=19)
abline(lm(z1 ~ x1), col="red", lwd=2, lty=1)

plot(x2, y2, main="Basic Scatterplot of Homeless vs. Negative Polarity",xlab="Polarity", ylab="Homeless", pch=19)
abline(lm(y2 ~ x2), col="red", lwd=2, lty=1)

plot(x2, z2, main="Basic Scatterplot of Homeless Trend vs. Negative Polarity",xlab="Polarity", ylab="Homeless Trend", pch=19)
abline(lm(z2 ~ x2), col="red", lwd=2, lty=1)

# fit a linear model of homeless trend predicted by polarity and homeless
polarity = tdata[, 1]
homeless = tdata[, 2]
homeless_t = tdata[, 3]

fit = lm(homeless_t ~ polarity + homeless + polarity:homeless)
summary(fit)
confint(fit)
