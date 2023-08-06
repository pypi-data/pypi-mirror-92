## Hardness measures adopted in Smith et al. 
## An Instance Level Analysis of Data Complexity - Machine Learning

##  kDN_measure(dataset,k) --- k-Disagreeing Neighbors (kDN)

##  TD_measure(dataset) --- Tree Depth (TD)
##   *** TD --- pruned tree (TD P) 
##   *** TU --- unpruned tree (TD U)
     
##  CL_measure(dataset)
##  *** CL --- Class Likelihood (CL)
##  *** CLD --- Class Likelihood Difference (CLD)

##  MV_measure(dataset) 
##  *** MV --- Minority Value (MV)
##  *** CB --- Class Balance (CB)

##  DS_measure(dataset) --- Disjunct Size (DS)

##  DSP_measure(dataset) --- Disjunct Class Percentage (DCP)

## HINTS
## TD: high values, high hardness
## kDN: high values, high hardness
## CL, CLD: low values, high hardness
## MV: high values, high hardness  
## CB: low values, high hardness
## DS: low values, high hardness
## DSP: low values, high hardness

########################################################
########################################################

library(rpart)
library(partykit)
library(stringr)

TD_measure <- function(dataset){
## Input: a data frame containing the training dataset 
## For each instance of the dataset, return the depth of the leaf node 
## that classifies the instance. Computed for both: prunned and unprunned trees.  
## Output: 
## --- TD: TD measure using a prunned tree
## --- TU: TD measure using an unprunned tree

 numInstances = nrow(dataset)
 numAtributes = ncol(dataset)

 names=names(dataset)
 formula = as.formula(paste(names[numAtributes],"~.")) 

 ## unpruned tree to use in the TU measure
 fit = rpart(formula, data = dataset,method='class',minsplit = 2,cp=0)

 ## pruned tree to use in the TD measure
 pruned_fit = rpart(formula, data = dataset,method='class')

  
 ## find the depth of terminal nodes of the UNPRUNED model
 
  terminal_ids = nodeids(as.party(fit),terminal=TRUE)
 
  list = partykit:::.list.rules.party(as.party(fit))
 
  depth = list()

  for(i in terminal_ids){

   rule = list[[toString(i)]]
   
   depth[[i]] = str_count(rule, "&") + 1

  }
  
  ## index of terminal node for each training example
  nodes = predict(as.party(fit), type = "node") 
  
  TD_U_all = unlist(depth[nodes])

  
  ## find the depth of terminal nodes of the PRUNED model
 
  terminal_ids = nodeids(as.party(pruned_fit),terminal=TRUE)
 
  list = partykit:::.list.rules.party(as.party(pruned_fit))
 
  depth = list()

  for(i in terminal_ids){

   rule = list[[toString(i)]]
   
   depth[[i]] = str_count(rule, "&") + 1

  }
  
  ## index of terminal node for each training example
  nodes = predict(as.party(pruned_fit), type = "node") 
  
  TD_P_all = unlist(depth[nodes])

  list(TD=TD_P_all,TU=TD_U_all)

}

########################################################
########################################################

library(FNN)

#kDN_measure <- function(dataset,k){
## For each instance, kDN is the percentage of the k nearest neighbors 
## (using Euclidean distance) for the instance that do
## not share its target class value.

# kDN_all = list()

# numInstances = nrow(dataset)
# numAtributes = ncol(dataset)

#   for (i in 1:numInstances){

     ## for each test instance i, split the training data
 
#     indTrain = setdiff(1:numInstances,i)

#     Train = dataset[indTrain,-numAtributes] # todos para treino
#     Test = dataset[i,-numAtributes] # um para teste

#     labelsTrain = factor(dataset[indTrain,numAtributes]) # labels dos dados de treinamento
 
#     labelTest = factor(dataset[i,numAtributes]) # label de teste
     ## levels(labelTest) = levels(dataset[,numAtributes])

     ## apply the knn
#     model = knn(Train,Test,labelsTrain,k=k,prob=TRUE) 

     ## retrieve the indices of the nearest neighbors  
#     indices <- attr(model, "nn.index")
     
#     labels_NN = dataset[indices,numAtributes]
     
     ## proportion of nn labels that are different to the class label of the test instance
#     kDN = length(which(as.vector(labels_NN) != as.vector(labelTest)))/k

#     kDN_all[[i]] = kDN

#   }
 
#   return(unlist(kDN_all))

#}

kDN_measure <- function(dataset,k){
  ## For each instance, kDN is the percentage of the k nearest neighbors 
  ## (using Euclidean distance) for the instance that do
  ## not share its target class value.
  
  kDN_all = list()
  
  numInstances = nrow(dataset)
  numAtributes = ncol(dataset)
  
  model <- knn.cv(dataset[,-numAtributes],as.factor(dataset[,numAtributes]),k,prob=TRUE)
  #kDN_all <- 1 - attr(model,"prob")
  indices <- attr(model, "nn.index")
  
  for (i in 1:numInstances){
    
    labels_NN <- dataset[indices[i,],numAtributes]
    labelTest <- dataset[i,numAtributes]
    ## proportion of nn labels that are different to the class label of the test instance
    kDN = length(which(as.vector(labels_NN) != as.vector(labelTest)))/k

    kDN_all[[i]] = kDN
    
  }
  
  return(unlist(kDN_all))
  #return(kDN_all)
  
}

########################################################
########################################################

library(e1071)

CL_measure <- function(dataset){
## CL measure: For each instance, it computes the likelihood of the
## instance belonging to its class

## CLD measure: For each instance, it computes the difference between the 
## class likelihood of an instance and the maximum likelihood for all of the other classes

numAtributes = ncol(dataset)
numInstances = nrow(dataset)

c = as.factor(dataset[,numAtributes])
labels = levels(c)

prob_prior = cbind()
for(k in 1:length(labels))
{

  pclass = length(which(dataset[,numAtributes]==labels[k]))/numInstances
  prob_prior = cbind(prob_prior, pclass)
}

model = naiveBayes(dataset[,-numAtributes],as.factor(dataset[,numAtributes])) 

CL_all = list()
CLD_all = list()


for(j in 1:numInstances)
{
  

  # choose the likelihood taking into account the target class of the instance
  target = dataset[j,numAtributes]

  prob = predict(model,dataset[j,-numAtributes],type="raw")

  aux = prob/prob_prior
  lhood = aux/(sum(aux))

  lhood_target = lhood[1,which(colnames(lhood)==target)]

  CLD = lhood_target - max(lhood[1,which(colnames(lhood)!=target)])

  CL_all[j] = lhood_target
  CLD_all[j] = CLD

} 

  list(CL=unlist(CL_all),CLD=unlist(CLD_all))


}

########################################################
########################################################

MV_measure <- function(dataset){
## For each instance, MV is the ratio of the number of instances sharing 
## its target class value to the number of instances in the majority class
## CB also measures the skewness of the class that an instance belongs
## to and offers an alternative to MV.

numAtributes = ncol(dataset)
numInstances = nrow(dataset)

c = as.factor(dataset[,numAtributes])
labels = levels(c)

num_prior = cbind()
num_classes = length(labels)

for(k in 1:num_classes)
{

  numclass = length(which(dataset[,numAtributes]==labels[k]))
  num_prior = cbind(num_prior, numclass)
}

max_prior = max(num_prior)

MV_all = cbind()
CB_all = cbind()


for(j in 1:numInstances)
{
  
  # choose the likelihood taking into account the target class of the instance
  target = dataset[j,numAtributes]
  ind_target = which(labels==target)

  MV = 1 - num_prior[ind_target]/max_prior 

  CB = num_prior[ind_target]/numInstances - 1/num_classes 

  MV_all = cbind(MV_all,MV)  
  CB_all = cbind(CB_all,CB)  
  
}

 list(MV = MV_all,CB = CB_all)

}


########################################################
########################################################

DS_measure <- function(dataset){
## DS of an instance is the number of instances in a disjunct (set of instances
## belonging to a leaf) divided by the 
## number of instances covered by the largest disjunct in a data set.

 numInstances = nrow(dataset)
 numAtributes = ncol(dataset)

 names=names(dataset)
 formula = as.formula(paste(names[numAtributes],"~.")) 

 fit = rpart(formula, data = dataset,method='class',minsplit = 1,cp=0)

 
 ## find the length of the disjunct for each terminal nodes of the UNPRUNED model
 
  ## indices of terminal nodes
  terminal_ids = nodeids(as.party(fit),terminal=TRUE)
 
  ## index of terminal node for each training example
  nodes = predict(as.party(fit), type = "node") 

  disjunct_size = cbind()

  for(i in terminal_ids){

   node_i = i
   disjunct_size = cbind(disjunct_size, length(which(nodes==node_i)))
   
  }
  
  max_disjunct_size = max(disjunct_size)
 
  DS_all = cbind()


  for(i in 1:numInstances){

     terminal_i = nodes[i]
     ind = which(terminal_ids==terminal_i)
     
     DS_i = (disjunct_size[ind]-1)/(max_disjunct_size - 1)

     DS_all = cbind(DS_all, DS_i)
  
   
  }
  
  return(DS_all)

}

########################################################
########################################################

DSP_measure <- function(dataset){
## The DCP of an instance is the number of instances in a disjunct 
## (set of instances in a leaf of a prunned tree) belonging to its class 
## divided by the total number of instances in the disjunct.

 numInstances = nrow(dataset)
 numAtributes = ncol(dataset)

 names=names(dataset)
 formula = as.formula(paste(names[numAtributes],"~.")) 

 fit = rpart(formula, data = dataset,method='class')

 
 ## find the length of the disjunct for each terminal nodes of the PRUNED model
 
  ## indices of terminal nodes
  terminal_ids = nodeids(as.party(fit),terminal=TRUE)
 
  ## index of terminal node for each training example
  nodes = predict(as.party(fit), type = "node") 

  disjunct_size = cbind()

  for(i in terminal_ids){

   node_i = i
   disjunct_size = cbind(disjunct_size, length(which(nodes==node_i)))
   
  }
 
  DSP_all = cbind()

  for(i in 1:numInstances){

     terminal_i = nodes[i]
     ind = which(terminal_ids==terminal_i)
     
     instances_node = which(nodes==terminal_i)

     same_class = length(which(dataset[instances_node,numAtributes] == dataset[i,numAtributes])) 

     DSP_i = same_class/disjunct_size[ind]
     DSP_all = cbind(DSP_all, DSP_i)

  }
  
  return(DSP_all)

}

########################################################
########################################################
