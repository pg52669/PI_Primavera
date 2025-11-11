#import "colors.typ"

#let render-cover(
  author: [],
  title: [],
  date: [],
  images: (),
  school: [],
  degree: []
) = [
  #set text(fill: colors.pantonecoolgray7)

  #set page(margin: (top: 0mm, bottom: 10mm, left: 79mm, right: 0mm))
  #set par(spacing: 0pt)

  #grid(
    columns: 2,
    ..images.map(block.with(width: 26mm, height: 26mm)),
  )

  #v(8.72mm)

  #[
    #set par(leading: 0.4em)
    #set text(size: 14.5pt)
    *Universidade do Minho*\
    #text(font: "NewsGoth Lt BT", school)
  ]

  #v(37.32mm)

  #place(top + left, float: false, dy: 90mm)[
    #set text(size: 17pt)
    #set par(leading: 20.4pt - 0.75em, spacing: 25pt)

    #author

    *#title*
  ]

  #align(bottom, text(size: 10pt, date))

]