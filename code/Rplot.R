# ! /usr/bin/Rscript

# opar <- par(no.readonly=TRUE)
pdf("../figure/1.pdf")
x <- c(0,2,4,6,8,10,12,14,16,18,20,22,24)
y <- c(0,600,1200,1800,2400,3000)
data1 <- read.table("../data/plot/R_trace_all", header=TRUE, stringsAsFactors=FALSE, sep=" ")
data2 <- read.table("../data/plot/R_trace_online", header=TRUE, stringsAsFactors=FALSE, sep=" ")
par(fig=c(0.05, 0.95, 0.2, 0.9))
boxplot(dura ~ time, data = data1, main = "Syslog", xlab = "Time of Day /h", ylab = "Time /s", xlim=c(0,24), ylim = c(0,3000), xaxt = "n", yaxt = "n")
# agg = aggregate(data1$dura, by=list(time=data1$time), mean)
# lines(agg$x, agg$dura, type="b", pch=3, col="black")
agg = aggregate(data2$dura, by=list(time=data2$time), mean)
lines(agg$x, agg$dura, type="b", pch=3, col="red")
# boxplot(dura ~ time, data = data2, col="red", add = TRUE)
legend("topleft", c("Online"), pch=c(3,3), col = c("red"))
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
dev.off()
# par(opar)

# opar <- par(no.readonly=TRUE)
pdf("../figure/2.pdf")
par(cex=0.65)
par(fig=c(0.05, 0.5, 0.6, 0.95))
x <- c(0,200,400,600,800,1000)
y <- c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)
data <- read.table("../data/host/http_host_ratio", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data$n, data$ratio, type="n", main="Cumulative Distribution of HTTP Host", xlab=" HTTP Host Ordinal Number", ylab="CDF", xlim=c(0,1000), ylim=c(0,1), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data$n, data$ratio)
par(fig=c(0.5, 0.95, 0.6, 0.95), new=TRUE)
data <- read.table("../data/host/http_host_top", header=TRUE, stringsAsFactors=FALSE, sep=" ")
barplot(structure(data$ratio, .Dim = c(5L), .Dimnames = list(data$host)), ylim=c(0,40), xaxt="n", main = "Ratio of HTTP Top Host", ylab = "Ratio %")
axis(1, at=c(0,1,2,3,4)*1.2+0.6, labels=data$host, las=2, cex=0.1)
par(fig=c(0.05, 0.5, 0.25, 0.6), new=TRUE)
x <- c(0,5,10,15,20)
y <- c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)
data <- read.table("../data/host/http_type_ratio", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data$n, data$ratio, type="n", main="Cumulative Distribution of Response Type", xlab="Response Type Ordinal Number", ylab="CDF", xlim=c(0,20), ylim=c(0,1), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data$n, data$ratio)
par(fig=c(0.5, 0.95, 0.25, 0.6), new=TRUE)
data <- read.table("../data/host/http_type_top", header=TRUE, stringsAsFactors=FALSE, sep=" ")
barplot(structure(data$ratio, .Dim = c(10L), .Dimnames = list(data$type)), ylim=c(0,40), xaxt="n", main = "Ratio of Top Response Type", ylab = "Ratio %")
axis(1, at=c(0,1,2,3,4,5,6,7,8,9)*1.2+0.6, labels=data$type, las=2, cex=0.1)
dev.off()
# par(opar)

# opar <- par(no.readonly=TRUE)
pdf("../figure/3.pdf")
par(cex=0.65)
par(fig=c(0.05, 0.5, 0.3, 0.8))
x <- c(1,50,100,150,200,250,300,350,400,450,500)
y <- c(100,200,300,400,500,600,700,800,900,1000)
data <- read.table("../data/url/keywords_mac_statistic", header=TRUE, stringsAsFactors=FALSE, sep=" ")
# with(data,smoothScatter(x, y, colramp = colorRampPalette(c("white", "Red")), main="Words Distribution", xlab="user / word", ylab="freq / user"))
plot(data$w, data$c, type="b", col="red", main="Number of users share one word", xlab="Words Ordinal Number", ylab="Users Count", xlim=c(0,500), ylim=c(0,1000), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
par(fig=c(0.5, 0.95, 0.3, 0.8), new=TRUE)
x <- c(1,100,200,300,400,500,600,700,800,900,1000)
y <- c(50,100,150,200,250,300,350,400,450,500)
data <- read.table("../data/url/keywords_frequency_statistic", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data$p, data$n, type="b", col="red", main="Number of words used by one user", xlab="Users Ordinal Number", ylab="Words Count", xlim=c(0,1000), ylim=c(0,500), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
dev.off()
# par(opar)

# opar <- par(no.readonly=TRUE)
pdf("../figure/4.pdf")
par(cex=0.65)
par(fig=c(0.05, 0.33, 0.3, 0.7))
barplot(structure(c(278, 186),.Dim = c(2L),.Dimnames = list(c("Male","Female"))), ylim=c(0,350), main="Gender", xlab="Gender", ylab="Number")
par(fig=c(0.3, 0.65, 0.3, 0.7), new=TRUE)
barplot(structure(c(301, 109, 54),.Dim = c(3L),.Dimnames = list(c("<=20","21~22",">=23"))), ylim=c(0,350), main="Age", xlab="Age", ylab="Number")
par(fig=c(0.6, 1.0, 0.3, 0.7), new=TRUE)
barplot(structure(c(128, 70, 30, 28, 27),.Dim = c(5L),.Dimnames = list(c("Top1","Top2","Top3","Top4","Top5"))), ylim=c(0,150), main="Collage", xlab="Collage", ylab="Number")
dev.off()
# par(opar)

library(car)
# opar <- par(no.readonly=TRUE)
pdf("../figure/5.pdf")
data <- read.table("../data/plot/R_trace_online_cor", header=TRUE, stringsAsFactors=TRUE, sep=" ")
scatterplotMatrix(~Acad+Teach+Lib+Soc+Ath|age, data=data, reg.line=FALSE, smooth=FALSE, spread=FALSE, main="Spatial Matrix Age")
dev.off()
# par(opar)

library(car)
# opar <- par(no.readonly=TRUE)
pdf("../figure/6.pdf")
data <- read.table("../data/plot/R_trace_http_cor", header=TRUE, stringsAsFactors=TRUE, sep=" ")
scatterplotMatrix(~renren+baidu+sina+qq+taobao|sex, data=data, pch=c(2,3), col=c("red","green"), reg.line=FALSE, smooth=FALSE, spread=FALSE, main="Cyber Matrix Gender")
dev.off()
# par(opar)

opar <- par(no.readonly=TRUE)
par(family='STKaiti',cex=1.0)
data <- read.table("../data/url/keywords_statistics", header=TRUE, stringsAsFactors=FALSE, sep=" ")
# par(fig=c(0.0, 0.5, 0.15, 0.85))
# symbols(data$M, data$F, circle=data$wt, inches=0.3, xlim=c(0.015,0.6), ylim=c(0.015,0.6), fg="white", bg="lightblue", main="Word Buble 2D", xlab="Male ratio", ylab="Female ratio")
# symbols(data$M, data$F, circle=data$wt^0.5, inches=0.1, xlim=c(0.015,0.55), ylim=c(0.015,0.55), fg="white", bg="lightblue", main="Words Occurrence Probability among Different Genders", xlab="Male", ylab="Female")
plot(data$M, data$F, xlim=c(0.015,0.55), ylim=c(0.015,0.55), main="Word Buble Gender", xlab="Male", ylab="Female", pch=1, col="lightblue")
text(data$M, data$F, data$wd, cex=0.65, pos=4, col="black")
lines(c(0,0.6),c(0,1), col="red", lty=2)
lines(c(0,1),c(0,0.5), col="red", lty=2)
# # par(fig=c(0.5, 1.0, 0.15, 0.85), new=TRUE)
# # symbols(data$A1, data$A3, circle=data$wt^0.5, inches=0.1, xlim=c(0.015,0.55), ylim=c(0.015,0.55), fg="white", bg="lightblue", main="Words Occurrence Probability among Different Ages", xlab="<21", ylab=">22")
# plot(data$A1, data$A3, xlim=c(0.015,0.55), ylim=c(0.015,0.55), main="Word Buble Age", xlab="<21", ylab=">22", pch=1, col="lightblue")
# text(data$A1, data$A3, data$wd, cex=0.65, pos=4, col="black")
# lines(c(0,0.6),c(0,1), col="red", lty=2)
# lines(c(0,1),c(0,0.5), col="red", lty=2)
par(opar)

opar <- par(no.readonly=TRUE)
par(family='STKaiti',cex=1.0)
data <- read.table("../data/url/bayes_sex", header=TRUE, stringsAsFactors=FALSE, sep=" ")
# par(fig=c(0.0, 0.5, 0.15, 0.85))
# symbols(data$M, data$F, circle=data$wt, inches=0.3, xlim=c(0.015,0.6), ylim=c(0.015,0.6), fg="white", bg="lightblue", main="Word Buble 2D", xlab="Male ratio", ylab="Female ratio")
# symbols(data$M, data$F, circle=data$wt^0.5, inches=0.1, xlim=c(0,0.001), ylim=c(0,0.001), fg="white", bg="lightblue", main="Word Buble Gender", xlab="Male", ylab="Female")
plot(data$M, data$F, xlim=c(0,0.002), ylim=c(0,0.002), main="Posterier Probability Comparison among Different Genders", xlab="Male", ylab="Female", pch=1, col="lightblue")
text(data$M, data$F, data$wd, cex=0.65, pos=4, col="black")
lines(c(0,0.6),c(0,1), col="red", lty=2)
lines(c(0,1),c(0,0.65), col="red", lty=2)
# # par(fig=c(0.5, 1.0, 0.15, 0.85), new=TRUE)
# # symbols(data$A1, data$A3, circle=data$wt^0.5, inches=0.1, xlim=c(0.015,0.55), ylim=c(0.015,0.55), fg="white", bg="lightblue", main="Word Buble Age", xlab="<21", ylab=">22")
# plot(data$A1, data$A3, xlim=c(0,0.003), ylim=c(0,0.003), main="Posterier Probability Comparison among Different Ages", xlab="<21", ylab=">22", pch=1, col="lightblue")
# text(data$A1, data$A3, data$wd, cex=0.65, pos=4, col="black")
# lines(c(0,0.6),c(0,1), col="red", lty=2)
# lines(c(0,1),c(0,0.65), col="red", lty=2)
par(opar)

# opar <- par(no.readonly=TRUE)
pdf("../figure/9.pdf")
par(cex=0.5)
par(fig=c(0.5, 0.95, 0.66, 1.0))
x <- c(10,100,200,300,400,500)
y <- c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1)
data <- read.table("../data/feature_set/dimension_accuracy", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data$dim, data$sex_a, type="b", pch=0, col="red", main="Gender", xlab="Feature Dimension", ylab="Accuracy", xlim=c(0,500), ylim=c(0,0.9), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data$dim, data$sex_o, type="b", pch=1, col="green")
lines(data$dim, data$sex_h, type="b", pch=2, col="blue")
abline(h=y,v=x,lty=2,col="grey")
legend("bottomright", inset=0, c("Spatial trajectory","Online trajectory","HTTP log"), pch=c(0,1,2), col=c("red","green","blue"))
par(fig=c(0.5, 0.95, 0.33, 0.67), new=TRUE)
x <- c(10,100,200,300,400,500)
y <- c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1)
data <- read.table("../data/feature_set/dimension_accuracy", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data$dim, data$age_a, type="b", pch=0, col="red", main="Age", xlab="Feature Dimension", ylab="Accuracy", xlim=c(0,500), ylim=c(0,0.9), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data$dim, data$age_o, type="b", pch=1, col="green")
lines(data$dim, data$age_h, type="b", pch=2, col="blue")
abline(h=y,v=x,lty=2,col="grey")
legend("bottomright", inset=0, c("Spatial trajectory","Online trajectory","HTTP log"), pch=c(0,1,2), col=c("red","green","blue"))
par(fig=c(0.5, 0.95, 0, 0.34), new=TRUE)
x <- c(10,100,200,300,400,500)
y <- c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1)
data <- read.table("../data/feature_set/dimension_accuracy", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data$dim, data$col_a, type="b", pch=0, col="red", main="College", xlab="Feature Dimension", ylab="Accuracy", xlim=c(0,500), ylim=c(0,0.9), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data$dim, data$col_o, type="b", pch=1, col="green")
lines(data$dim, data$col_h, type="b", pch=2, col="blue")
abline(h=y,v=x,lty=2,col="grey")
legend("bottomright", inset=0, c("Spatial trajectory","Online trajectory","HTTP log"), pch=c(0,1,2), col=c("red","green","blue"))
par(fig=c(0.05, 0.5, 0.66, 1.0), new=TRUE)
x <- c(0,50,100,150,200,250,300,350,400,450,500)
y <- c(0,2,4,6,8,10,12)
data1 <- read.table("../data/feature_set/feature_set_all_sex_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
data2 <- read.table("../data/feature_set/feature_set_online_sex_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
data3 <- read.table("../data/feature_set/feature_set_http_sex_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data1$p, data1$s, type="l", pch=0, col="red", main="Gender", xlab="Feature Dimension", ylab="p-Score", xlim=c(0,500), ylim=c(0,12), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data2$p, data2$s, type="l", pch=1, col="green")
lines(data3$p, data3$s, type="l", pch=2, col="blue")
legend("topright", inset=0, c("Spatial trajectory","Online trajectory","HTTP log"), pch=c(0,1,2), col=c("red","green","blue"))
par(fig=c(0.05, 0.5, 0.33, 0.67), new=TRUE)
x <- c(0,50,100,150,200,250,300,350,400,450,500)
y <- c(0,10,20,30,40)
data1 <- read.table("../data/feature_set/feature_set_all_age_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
data2 <- read.table("../data/feature_set/feature_set_online_age_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
data3 <- read.table("../data/feature_set/feature_set_http_age_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data1$p, data1$s, type="l", pch=0, col="red", main="Age", xlab="Feature Dimension", ylab="p-Score", xlim=c(0,500), ylim=c(0,40), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data2$p, data2$s, type="l", pch=1, col="green")
lines(data3$p, data3$s, type="l", pch=2, col="blue")
legend("topright", inset=0, c("Spatial trajectory","Online trajectory","HTTP log"), pch=c(0,1,2), col=c("red","green","blue"))
par(fig=c(0.05, 0.5, 0, 0.34), new=TRUE)
x <- c(0,50,100,150,200,250,300,350,400,450,500)
y <- c(0,10,20,30,40,50)
data1 <- read.table("../data/feature_set/feature_set_all_col_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
data2 <- read.table("../data/feature_set/feature_set_online_col_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
data3 <- read.table("../data/feature_set/feature_set_http_col_500", header=TRUE, stringsAsFactors=FALSE, sep=" ")
plot(data1$p, data1$s, type="l", pch=0, col="red", main="College", xlab="Feature Dimension", ylab="p-Score", xlim=c(0,500), ylim=c(0,50), xaxt="n", yaxt="n")
axis(1, at=x, labels=x)
axis(2, at=y, labels=y)
lines(data2$p, data2$s, type="l", pch=1, col="green")
lines(data3$p, data3$s, type="l", pch=2, col="blue")
legend("topright", inset=0, c("Spatial trajectory","Online trajectory","HTTP log"), pch=c(0,1,2), col=c("red","green","blue"))
dev.off()
# par(opar)

# opar <- par(no.readonly=TRUE)
par(cex=0.7)
pdf("../figure/10.pdf")
par(fig=c(0.15, 0.85, 0.3, 0.8))
tmp = structure(c(
	0.6897, 0.7240, 0.8017, 0.8491, 
	0.8298, 0.8091, 0.6142, 0.8491,
	0.7916, 0.4417, 0.4170, 0.8198
	),
	.Dim = c(4L, 3L),
	.Dimnames = list(c("S_a","Cy", "Se","Co"),c("Gender", "Age", "College")))
barplot(tmp, ylim = c(0,1), col = c("brown1","orange","yellow","chartreuse"), beside = TRUE, main = "Accuracy", xlab = "Task", ylab = "Accuracy", las = 1)
legend(9.75,0.98, c("Spatial","Cyber","Semantic", "Integrated"), pch=c(15,15,15,15), col = c("brown1","orange","yellow","chartreuse"))
dev.off()
# par(opar)
