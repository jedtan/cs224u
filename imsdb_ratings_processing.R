require(ggplot2)
imsdb_ratings = read.csv("/Users/tdliu/Documents/cs224u/project/cs224u/imsdb_ratings.csv", header = FALSE, stringsAsFactors = FALSE)
for (i in 3:ncol(imsdb_ratings)){
  imsdb_ratings[,i] <- as.numeric(imsdb_ratings[,i])
}
names(imsdb_ratings) <- c('name', 'genre', 'imdb_rating', 'metascore', 'tomato_rating', 'tomato_reviews', 'tomato_fresh','tomato_rotten', 'tomato_user_meter', 'tomato_user_rating')
# Metacritic ratings
imsdb_ratings$tomato_meter <- 100*imsdb_ratings$tomato_fresh/(imsdb_ratings$tomato_fresh + imsdb_ratings$tomato_rotten)
qplot(imsdb_ratings$V4, geom = "histogram")

ggplot(imsdb_ratings, aes(x=tomato_meter)) + geom_density()

# data set right-skewed. less strict threshold requirement for lower bound, stricter threshold requirement of upper bound

sum(imsdb_ratings$tomato_meter <= 50, na.rm = TRUE)
sum(imsdb_ratings$tomato_meter >= 90, na.rm = TRUE)
summary(imsdb_ratings$tomato_meter)

# table with only name genre and tomato meter rating with min number of reviews
df <- imsdb_ratings[,c('name', 'genre', 'tomato_reviews', 'tomato_meter')]
df <- df[complete.cases(df),]

binary_quality <- rep(NA, nrow(df))
binary_quality[df$tomato_meter >= 90] <- 1
binary_quality[df$tomato_meter <= 50] <- 0
df$binary_quality <- binary_quality

final_df <- df[complete.cases(df),]

write.csv(final_df, "/Users/tdliu/Documents/cs224u/project/cs224u/imsdb_ratings_processed.csv", row.names = FALSE, col.names= FALSE)






