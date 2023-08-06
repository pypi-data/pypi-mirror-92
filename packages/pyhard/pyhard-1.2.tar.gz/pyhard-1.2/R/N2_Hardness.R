normalize <- function(x) {
  return ((x - min(x)) / (max(x) - min(x))) }

dist <- function(x) {
  as.matrix(cluster::daisy(x, metric="gower", stand=TRUE))
}

data <- data.frame(x, class=y)

dst <- dist(x)

intra <- function(dst, data, i) {
  tmp <- rownames(data[data$class == data[i,]$class,])
  aux <- min(dst[i, setdiff(tmp, i)])
  return(aux)
}

inter <- function(dst, data, i) {
  tmp <- rownames(data[data$class != data[i,]$class,])
  aux <- sort(dst[i, tmp])[1]
  #print(aux)
  return(aux)
}

c.N2 <- function(dst, data) {
  
  aux <- sapply(rownames(data), function(i) {
    c(intra(dst, data, i), inter(dst, data, i))
  })
  
  aux <- (aux[1,])/(aux[2,])
  #aux <- 1 - (1/(aux + 1))
  return(aux)
}