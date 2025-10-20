// main project
#let project(
  title: "",
  subtitle: "",
  author: "",
  affiliation: "",
  Licence: none,
  UE: none,
  date: none,
  logo: none,
  main_color: "000000",
  alpha: 60%,
  toc_title: "Table des matières",
  body,
) = {
  // Set the document's basic properties.
  set document(author: author, title: title)

  // Save heading and body font families in variables.
  let body-font = "Rethink Sans"
  let sans-font = "Open Sans"

  // Set colors
  let primary-color = rgb(main_color) // alpha = 100%
  // change alpha of primary color
  let secondary-color = color.mix(color.rgb(100%, 100%, 100%, alpha), primary-color, space: rgb)

  set page(margin: (
    top: 2.5cm,
    bottom: 2.5cm,
    right: 2cm,
    left: 2cm,
  ))

  show "highlight": it => text(fill: primary-color)[#it]

  //customize look of figure
  set figure.caption(separator: [ --- ], position: bottom)

  //customize inline raw code
  show raw.where(block: false): it => (
    h(0.5em)
      + box(
        fill: rgb(240, 240, 240),
        radius: 4pt,
        inset: 0.3em,
        it,
      )
      + h(0.5em)
  )

  // Set body font family.
  set text(font: body-font, lang: "fr", 11.5pt)
  show heading: set text(font: sans-font, fill: primary-color)

  //heading numbering
  set heading(numbering: "1.")

  // Set link style
  show link: it => underline(text(fill: primary-color, it))

  //pagebreak before first heading and space after
  //show heading.where(level:1): it => pagebreak(weak: true) + it + v(0.5em)

  // no pagebreak before heading
  show heading.where(level: 1): it => it + v(0.5em)

  //numbered list colored
  set enum(indent: 1em, numbering: n => [#text(fill: primary-color, numbering("1.", n))])

  //unordered list colored
  set list(indent: 1em, marker: n => [#text(fill: primary-color, "•")])


  // display of outline entries
  show outline.entry: it => text(size: 12pt, weight: "regular", it)

  //avoid C++ word break
  show "C++": box

  // Title page.
  // Logo at top right if given
  if logo != none {
    place(top + left, image(logo, width: 20%))
  }
  // decorations at top left
  // place(top + left, dx: -35%, dy: -28%, circle(radius: 150pt, fill: primary-color))
  // place(top + left, dx: -10%, circle(radius: 75pt, fill: secondary-color))

  // // decorations at bottom right
  // place(bottom +right, dx: 40%, dy: 30%, circle(radius: 150pt, fill: secondary-color))


  v(2fr)

  align(center, text(font: sans-font, 3em, weight: 700, title))
  v(2em, weak: true)
  align(center, text(font: sans-font, 2em, weight: 700, subtitle))
  v(2em, weak: true)
  align(center, text(1.1em, date))

  v(2fr)

  // Author information.
  align(center)[
    #text(author, 14pt, weight: "bold") \
    #affiliation \ #Licence\ #emph[#UE]
  ]

  pagebreak()


  // Table of contents.
  set page(
    numbering: "1 / 1",
    number-align: center,
  )
  outline(depth: 3, indent: 1em, title: toc_title)
  //useless pagebreak because using pagebreak before first heading and assuming that the page always starts with a heading
  //pagebreak()


  // Main body.
  set page(
    // header: [#emph()[#title #h(1fr) #author]],
    // header: [#grid(
    //   columns: (1fr, 1fr, 1fr),
    //   rows: (auto),
    //   [#align(left, emph(title))], [#align(top + center, subtitle)], [#align(top+ right,author)]
    // )]
  )
  set par(justify: true)

  body
}

//useful functions

