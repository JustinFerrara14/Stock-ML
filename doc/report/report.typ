
#import "template.typ": *
#import "@preview/codelst:2.0.0": sourcecode
#import "@preview/wrap-it:0.1.1": wrap-content

#show: project.with(
  title: "TSM-MachLeData",
  subtitle: "Stock Price Prediction using Machine Learning",
  author: "Justin Ferrara
  Luca Da Silva
  Rafael Cardoso
  Thomas Maksimous",
  affiliation: "HES-SO Master",
  date: datetime(year: 2025, month: 10, day: 20).display("[day].[month].[year]"),
  Licence: "-",
  logo: "assets/HES_SO_Logo_RGB.png",
  toc_title: "Table of Contents",
)

//set block-quote
#let blockquote = rect.with(stroke: (left: 2.5pt + luma(170)), inset: (left: 1em))
#let primary-color = rgb("E94845")
#let secondary-color = rgb(255, 80, 69, 60%)

#show raw.where(block: true): block.with(
  fill: rgb(240, 240, 240), // Fond gris clair
  inset: 8pt, // Marge intérieure
  radius: 4pt, // Coins arrondis
  width: 100%, // Largeur
)
#show raw.where(block: true): set text(font: "Source Code Pro")

#pagebreak()

= Introduction

TODO

#pagebreak()

= Project Scoping

TODO

= Data Engineering

TODO

= ML Model Development

TODO

= Deployment

TODO

= Monitoring

TODO

= Business Analysis

TODO

= Conclusion

TODO
