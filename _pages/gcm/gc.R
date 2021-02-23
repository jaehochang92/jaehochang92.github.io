library(dplyr)
library(ggplot2)
library(lubridate)
library(reticulate)
library(extrafont)
Sys.setenv(RETICULATE_PYTHON = "/usr/local/Caskroom/miniconda/base/bin/python")
gc.mon <- function(query, prgrm = 'PhD') {
  writeLines(query, 'query.txt')
  source_python('main.py', NULL)
  gc <- read.csv('tmp.csv')
  colnames(gc)
  tab <- gc %>%
    filter(
      stringr::str_detect(과정, prgrm) &
        stringr::str_detect(결과, 'Accepted|Rejected|Wait listed')
    ) %>%
    mutate(on = strptime(on, '%d %b %Y') %>% ymd,
           게시날짜 = strptime(게시날짜, '%d %b %Y') %>% ymd) %>%
    arrange(desc(on))
  return(tab)
}

# Duke --------------------------------------------------------------------


(df <- gc.mon('duke bio*'))

suppressWarnings({
  df %>% group_by(결과, on) %>% summarise(cnt = n()) %>%
    ggplot(aes(x = on, y = cnt, col = 결과)) +
    geom_point() + scale_x_date(date_labels = "%b-%d-%Y") +
    theme_minimal(base_family = 'AppleGothic')
})
