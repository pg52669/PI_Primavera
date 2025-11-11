#import "src/lib.typ": colors, formatting, paper

#show: paper(
  authors: "Author, Author, Author",
  title: "App Social",
  date: [september 2025],
  cover-images: (image("logos/uminho/color/UM.jpg"), image("logos/uminho/color/EE.jpg")),
  school: [Escola de Engenharia],
  degree: [Projeto de Engenharia Informatica],
)


// Setup index
#import "@preview/in-dexter:0.7.2": *

#formatting.show-preamble[
  #outline()
  #pagebreak()
  #outline(title: [Lista de Figuras], target: figure.where(kind: image))
  #pagebreak()
  #outline(title: [Lista de tabelas], target: figure.where(kind: table))
  #pagebreak()
]

#show: formatting.show-main-content

= Material Introdutorio

== Introdução

=== Contexto
Social isolation and loneliness have been identified as significant public health concerns, with numerous studies highlighting their detrimental effects on mental and physical health. According to a comprehensive meta-analysis by Wang et al. (2023), social isolation and loneliness are associated with increased mortality rates, comparable to other well-known risk factors such as smoking and obesity. This underscores the urgent need for effective interventions to mitigate these issues.
Wang, F., Gao, Y., Han, Z., Yu, Y., Long, Z., Jiang, X., Wu, Y., Pei, B., Cao, Y., Ye, J., Wang, M., & Zhao, Y. (2023). A systematic review and meta-analysis of 90 cohort studies of social isolation, loneliness and mortality. Nature human behaviour, 7(8), 1307–1319. https://doi.org/10.1038/s41562-023-01617-6
=== Objetivos
Temos como objetivo desenvolver uma aplicação móvel que facilite a conexão entre indivíduos, promovendo interações sociais significativas e reduzindo a sensação de isolamento. A aplicação visa criar uma plataforma intuitiva e acessível, onde os usuários possam encontrar e participar de atividades sociais, grupos de interesse e eventos locais. A app será também um centro de informação de eventos comunitários, proporcionando aos usuários oportunidades para se envolverem com a sua comunidade local.

=== Motivação
Durante a operação "Censos Sénior 2023", da GNR foram sinalizados 44.114 idosos, que vivem sozinhos e/ou isolados ou que estão em situação de vulnerabilidade. Estes dados evidenciam a necessidade de soluções que promovam a inclusão social e o bem-estar dos idosos. A app social pretende ser uma ferramenta eficaz para combater o isolamento social, oferecendo uma plataforma onde os idosos possam facilmente encontrar e participar em atividades sociais, grupos de interesse e eventos locais, promovendo assim um envelhecimento ativo e saudável.

https://expresso.pt/lusa/2023-11-03-GNR-sinalizou-mais-de-44.100-idosos-que-vivem-sozinhos-ou-isolados-25b9183a

== Metodologia

= Trabalho feito

== Apresentação do  App Social

== Conclusão e Trabalhos Futuros


=== Conclusão

=== Trabalho Futuro



#formatting.show-postamble[
  // Render bibliography
  // Change this to a .bib file if you prefer that format instead
  #bibliography("bibliography.yml", full: true)

  
]


#set page(numbering: none)

