#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  startTime <- proc.time()

  output$distPlot <- renderPlot({
    #Read File
    n = input$bins
    data <- read.csv("C:/Users/Administrator/Desktop/data1.csv")
    #plot(age ~ height, data)
    a <- data[,-c(1,4,5,6,7)]

    #For normalizing
    ascale <- scale(a)
    set.seed(42)
    kmc <- kmeans(a, n)
    # Creating Table
    # ggplot(data=subTable) + geom_bar(mapping = aes(x= age))
    #plotting Cluster
    beginning <- Sys.time()
    plot(a, col=kmc$cluster, frame = FALSE, pch = 3)
    points(kmc$centers, col = 1:2, pch = 5, cex = 3)
    points(kmc$centers, col="green")
    plot(a,kmc$centers)
    #lines(kmc$centers, col="red")
    end <- Sys.time()
    print(end - beginning)
    
    #df <- kmc$cluster[order(kmc$centers,decreasing = TRUE)]

    #barplot(kmc$centers, main="My Barchart",legend.text=rownames(kmc$cluster),beside=TRUE,col=kmc$centers)
     #barplot(kmc$centers,legend.text=rownames(kmc$centers),beside=TRUE,names.arg =kmc$centers)
    j<-0

    #barplot(result$centers, main="Car Distribution", xlab="Number of Gears")
    for (i in 1:n){
      k <- i+1
      if(!( k>n))
        for( j in k:n){
          print(paste("Cluster Size = ",i, j))
          m<- i+n
          l<- j+n
          print(sqrt( (kmc$centers[i]-  kmc$centers[j])^2 +(kmc$centers[m]-  kmc$centers[l])^2))
        }
    }

  })
})