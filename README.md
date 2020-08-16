<!-- Inspired on https://github.com/othneildrew/Best-README-Template/blob/master/README.md-->

<!-- PROJECT SHIELDS -->

[![Issues][a1]][a1]
[![Stars][a2]][a2]
[![Forks][a3]][a3]
[![License][a4]][a4]
[![All Contributors][a5]][a5]

[a1]: https://img.shields.io/github/issues/DataScienceResearchPeru/covid-19_latinoamerica?style=for-the-badge
[a2]: https://img.shields.io/github/stars/DataScienceResearchPeru/covid-19_latinoamerica?style=for-the-badge
[a3]: https://img.shields.io/github/forks/DataScienceResearchPeru/covid-19_latinoamerica?style=for-the-badge
[a4]: https://img.shields.io/badge/License-CC%20BY--NC--SA-green?style=for-the-badge&logo=appveyor
[a5]: https://img.shields.io/badge/all_contributors-17-orange.svg?style=for-the-badge

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="#">
    <img src="https://github.com/othneildrew/Best-README-Template/raw/master/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Latin America Covid-19 Data Repository by DSRP </h3>

  <p align="center">
    Repository with daily updates related to Covid-19 of Latin America (South America)<br />
    <a href="https://latin-america-covid-19-repository.readthedocs.io/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://datastudio.google.com/u/2/reporting/9b824956-4055-46da-8c40-0d46ded5ffba/page/QkcKB">View Map</a>
    ·
    <a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/archive/master.zip">Download data</a>
    ·
    <a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica_extra">Extra data</a>
    <br />
    <a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/issues/new/choose">Request Feature</a>
    ·
    <a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/issues/new/choose">Data Error</a>

  </p>
  <p align="center">
  <a href="https://covid19latam.herokuapp.com/">API</a>
   ·
  <a href="https://github.com/rafnixg/covid-19_latinoamerica_api">API Repository</a>
   
  <p align="center">
  <!-- <br> -->
  <!-- <a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/issues/new/choose">I want to contribute</a>
   (Necesitamos colaboradores urgentemente) -->
  </p>
  <!-- <br> -->
  <p align="center">
  <a href="https://join.slack.com/t/covid19latinoamerica/shared_invite/zt-d99sp09d-mcwZ3AmFI_kmj~kYryg74w">¡Join our Slack!</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Tabla 1. Data resources for each country](#table1)
  - [Table 2. First date confirmed cases per country](#table2)
- [Projects](#projects)
- [Contributing](#contributing)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

<!-- ABOUT THE PROJECT -->

## About The Project

<p align="center">
<img src="old/docs/map.jpg" alt="Map" width="100%" >
</img>
</p>

<p align="center">
<br>
MAP <a href="https://datastudio.google.com/u/2/reporting/9b824956-4055-46da-8c40-0d46ded5ffba/page/QkcKB">Desktop version</a>
</br>
<br>
MAP <a href="https://datastudio.google.com/reporting/c817609e-3351-4614-acb7-3e72fdbc6d6a/page/QkcKB">Mobile version</a>
</br>
<br>
This repository is a part of <a href="https://www.notion.so/covid19dsrp/Per-Covid19-20068e871337453f93172b7b52e83261">various projects</a>
</br>
</p>

WARNING: Some countries are not reporting their death and recovery figures to the resolution we have in the repository.

#### Tabla 1. Data resources for each country

| #   | Country                  | User                                                                                                                | Data Sources                                                                                                        |
| --- | ------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1   | ARGENTINA                | [martingra](https://bit.ly/2UA5JjF) [pablorea](https://bit.ly/3dHNlwG) [Automated - ZurMaD](https://bit.ly/2wZwntr) | [D1](https://bit.ly/3aabv0y) [D2](https://bit.ly/394NsPy) [S1](https://bit.ly/2AHBPlX)                              |
| 2   | BOLIVIA                  | [mamanipatricia](https://bit.ly/2UzdbLU) [Automated - ZurMaD](https://bit.ly/2wZwntr)                               | [D1](https://bit.ly/3bh1qz6) [S1](https://bit.ly/2xPmjTx)                                                           |
| 3   | BRAZIL                   | [Automated - dfuribez](https://bit.ly/3aN3xLc) [Automated - ZurMaD](https://bit.ly/2wZwntr)                         | [S1](https://bit.ly/2xMr5kR) [D1](https://bit.ly/2WuChNd)                                                           |
| 4   | CHILE                    | [Automated - ivanMSC](https://bit.ly/2UZBUb6)                                                                       | [D1](https://bit.ly/2xWXhlH) [D2](https://bit.ly/02Jg6JDf) [D3](https://bit.ly/30AOaTE)                                                         |
| 5   | COLOMBIA                 | [Automated - dfuribez](https://bit.ly/3aN3xLc) [Automated - ZurMaD](https://bit.ly/2wZwntr)                         | [S1](https://bit.ly/39LPi8n) [D1](https://bit.ly/2xkYD9k) [D2](https://bit.ly/2UsSu2U)                              |
| 6   | COSTA RICA               | [Automated - dfuribez](https://bit.ly/3aN3xLc) [Automated - ZurMaD](https://bit.ly/2wZwntr)                         | [API](https://bit.ly/2V34zfz)                                                                                       |
| 7   | CUBA                     | [yudivian](https://bit.ly/2wVSYqL) [Automated - ZurMaD](https://bit.ly/2wZwntr)                                     | [API](https://bit.ly/2JGSA1Z) [S1](https://bit.ly/2AFqeDU)                                                          |
| 8   | DOMINICAN REPUBLIC       | [ZurMaD](https://bit.ly/2wZwntr)                                                                                    | [D1](https://bit.ly/2UKoUY9) [D2](https://bit.ly/2J2aBHM)                                                           |
| 9   | ECUADOR                  | [pablora19](https://bit.ly/2UB6rgl) [Automated - ZurMaD](https://bit.ly/2wZwntr)                                    | [D1](https://bit.ly/2J3ompB) [D2](https://bit.ly/2UsK2R7) [S1](https://bit.ly/2ADB39y)                              |
| 10  | EL SALVADOR              | [Automated - ZurMaD](https://bit.ly/2wZwntr)                                                                        | [D1](https://bit.ly/2U7N7Hm) [D2](https://bit.ly/39JhgBn)                                                           |
| 11  | FRENCH GUIANA            | WITHOUT MAINTENANCE                                                                                                 | [D1](https://bit.ly/2UUZsxU)                                                                                        |
| 12  | GUADELOUPE               | WITHOUT MAINTENANCE                                                                                                 | [D1](https://bit.ly/2V0aQsj)                                                                                        |
| 13  | GUATEMALA                | [ncovgt2020](https://bit.ly/3aHpECQ)                                                                                |                                                                                                                     |
| 14  | HAITI                    | WITHOUT MAINTENANCE                                                                                                 |                                                                                                                     |
| 15  | HONDURAS                 | [Automated - ivanMSC](https://bit.ly/2UZBUb6)                                                                       | [D1](https://bit.ly/2UQBDs5)                                                                                        |
| 16  | MARTINIQUE               | WITHOUT MAINTENANCE                                                                                                 | [D1](https://bit.ly/34fbNRW)                                                                                        |
| 17  | MEXICO                   | [Automated - carranco-sga](https://bit.ly/2UAAdSw)                                                                              | [D1](https://bit.ly/3brQ7nY)                                                                                        |
| 18  | NICARAGUA                | WITHOUT MAINTENANCE                                                                                                 | [D1](https://bit.ly/2QQNfJB)                                                                                        |
| 19  | PANAMA                   | [josetup123](https://github.com/josetup123)                                                                         | [D1](https://bit.ly/2UpH8he)                                                                                        |
| 20  | PARAGUAY                 | WITHOUT MAINTENANCE                                                                                                 |                                                                                                                     |
| 21  | PERU                     | [Automated - ZurMaD](https://bit.ly/2wZwntr) [diegocl02](https://bit.ly/2wNIlGt)                                    | [D1](https://bit.ly/2J5Wnpj) [D2](https://bit.ly/3dSKwZO) [D3](https://bit.ly/2StGIoL) [D4](https://bit.ly/3cCg5Gc) |
| 22  | PUERTO RICO              | WITHOUT MAINTENANCE                                                                                                 |                                                                                                                     |
| 23  | SAIN PIERRE AND MIQUELON | WITHOUT MAINTENANCE                                                                                                 |                                                                                                                     |
| 24  | SAINT BARTHELEMY         | WITHOUT MAINTENANCE                                                                                                 |                                                                                                                     |
| 25  | SAINT MARTIN             | WITHOUT MAINTENANCE                                                                                                 |                                                                                                                     |
| 26  | URUGUAY                  | WITHOUT MAINTENANCE                                                                                                 |                                                                                                                     |
| 27  | VENEZUELA                | [rendergraf](https://bit.ly/345Z2Jg)                                                                                | [D1](https://bit.ly/2J3E0Br) [D2](https://bit.ly/3acdykY)                                                           |

\*Automated by scripts in [this folder](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/tree/master/utils/scripts)

Table 2 moved to [First cases per country](utils/first_cases_date.csv) / [Last Update per country](utils/last_update_daily_report.csv)

See in [Google Sheets](https://bit.ly/3aEyAZI)

![Primer caso anunciado por país](https://imgur.com/zCegf9o.jpg)

<!-- GETTING STARTED -->

<!--
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- npm

```sh
npm install npm@latest -g
```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo

```sh
git clone https://github.com/your_username_/Project-Name.git
```

3. Install NPM packages

```sh
npm install
```

4. Enter your API in `config.js`

```JS
const API_KEY = 'ENTER YOUR API';
```
-->

<!-- USAGE EXAMPLES -->

<!-- ## Projects


<p align="center">

All commits on this repo: <br>
![DSRP](old/docs/dsrp.gif)<br>

REST API para programadores disponible aquí:
<a href="https://covid19latam.herokuapp.com/">API</a>
</p>
<p align="center">
Github Repo del REST API:
<a href="https://github.com/rafnixg/covid-19_latinoamerica_api">API</a>
</p> -->

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

This project exists thanks to all the people who contribute. [[Contribute](.github/CONTRIBUTING.md)]

If the country don't have a maintainer (see Table 1):

1. Contact us, we will give you `Maintainer` permission to commit freely.

If the country have a maintainer (see Table 1):

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- USAGE -->

## Usage

How to load data in Colab with python 3: [Google Colab - Code](https://bit.ly/3bJPuGM)

Other [scripts here](utils\scripts)

<!-- CONTACT -->

## Extra


[Extra data with orther important variables](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica_extra)

## Q&A

- **How to use data?**

Due to the amount of missing data, we recommend that only the `Confirmed` and `Deaths` columns be used. In the `daily_report` folder are the files for each day, there is a column called `Last Update`, we recommend removing it because it is for an internal purpose and is not relevant for any other purpose.

- **Is there a easy way to load all of your data to dataframes?**

Yes, we actually recommend this [notebook](https://bit.ly/3bJPuGM)

- **How can I know which countries are updated each day?**

By now, Perú, Chile, Honduras and Brazil are automated.
Others, not yet.

<!-- ACKNOWLEDGEMENTS -->

<!--
## Acknowledgements

- [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
- [Img Shields](https://shields.io)
- [Choose an Open Source License](https://choosealicense.com)
- [GitHub Pages](https://pages.github.com)
- [Animate.css](https://daneden.github.io/animate.css)
- [Loaders.css](https://connoratherton.com/loaders)
- [Slick Carousel](https://kenwheeler.github.io/slick)
- [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
- [Sticky Kit](http://leafo.net/sticky-kit)
- [JVectorMap](http://jvectormap.com)
- [Font Awesome](https://fontawesome.com)

-->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/ZurMaD"><img src="https://avatars2.githubusercontent.com/u/28235457?v=4" width="100px;" alt=""/><br /><sub><b>ZurMaD</b></sub></a><br /><a href="#design-ZurMaD" title="Design">🎨</a> <a href="#projectManagement-ZurMaD" title="Project Management">📆</a></td>
    <td align="center"><a href="https://github.com/carranco-sga"><img src="https://avatars2.githubusercontent.com/u/32427033?v=4" width="100px;" alt=""/><br /><sub><b>Gabriel Alfonso Carranco-Sapiéns</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=carranco-sga" title="Documentation">📖</a></td>
    <td align="center"><a href="http://rafnixg.xyz"><img src="https://avatars2.githubusercontent.com/u/10915285?v=4" width="100px;" alt=""/><br /><sub><b>Rafnix Guzman</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=rafnixg" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/RcrdPhysics"><img src="https://avatars0.githubusercontent.com/u/43417707?v=4" width="100px;" alt=""/><br /><sub><b>RcrdPhysics</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=RcrdPhysics" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/pablora19"><img src="https://avatars0.githubusercontent.com/u/62561297?v=4" width="100px;" alt=""/><br /><sub><b>Pablo Reyes A</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=pablora19" title="Documentation">📖</a></td>
    <td align="center"><a href="http://martingramatica.me"><img src="https://avatars2.githubusercontent.com/u/7132263?v=4" width="100px;" alt=""/><br /><sub><b>Martin</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=martingra" title="Documentation">📖</a></td>
    <td align="center"><a href="http://patriciamq.xyz"><img src="https://avatars2.githubusercontent.com/u/19600504?v=4" width="100px;" alt=""/><br /><sub><b>patty</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=mamanipatricia" title="Documentation">📖</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://cdn-images-1.medium.com/max/1200/0*JNGqpfzJUETMz9gE."><img src="https://avatars1.githubusercontent.com/u/830054?v=4" width="100px;" alt=""/><br /><sub><b>Leytzher</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=leytzher" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/josetup123"><img src="https://avatars2.githubusercontent.com/u/52168695?v=4" width="100px;" alt=""/><br /><sub><b>josetup123</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=josetup123" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/ivanMSC"><img src="https://avatars0.githubusercontent.com/u/35350256?v=4" width="100px;" alt=""/><br /><sub><b>ivang</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=ivanMSC" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/diegocl02"><img src="https://avatars1.githubusercontent.com/u/24798804?v=4" width="100px;" alt=""/><br /><sub><b>Diego Cisneros</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=diegocl02" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/dfuribez"><img src="https://avatars1.githubusercontent.com/u/28516148?v=4" width="100px;" alt=""/><br /><sub><b>Diego Fernando Uribe</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=dfuribez" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/carranco-sga"><img src="https://avatars2.githubusercontent.com/u/32427033?v=4" width="100px;" alt=""/><br /><sub><b>Gabriel Alfonso Carranco-Sapiéns</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=carranco-sga" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/ariasbordahugo"><img src="https://avatars0.githubusercontent.com/u/56813329?v=4" width="100px;" alt=""/><br /><sub><b>ariasbordahugo</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=ariasbordahugo" title="Documentation">📖</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/adtor97"><img src="https://avatars0.githubusercontent.com/u/53233704?v=4" width="100px;" alt=""/><br /><sub><b>adtor97</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=adtor97" title="Documentation">📖</a></td>
    <td align="center"><a href="https://pablorea.github.io/me/"><img src="https://avatars1.githubusercontent.com/u/25037383?v=4" width="100px;" alt=""/><br /><sub><b>Pablo Leandro Rea</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=pablorea" title="Documentation">📖</a></td>
    <td align="center"><a href="https://developers.ninja"><img src="https://avatars2.githubusercontent.com/u/5533099?v=4" width="100px;" alt=""/><br /><sub><b>Xavier Araque</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=rendergraf" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/ncovgt2020"><img src="https://avatars0.githubusercontent.com/u/62212482?v=4" width="100px;" alt=""/><br /><sub><b>Corona Virus Guatemala</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=ncovgt2020" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/Caospierre"><img src="https://avatars2.githubusercontent.com/u/20137969?v=4" width="100px;" alt=""/><br /><sub><b>Jean Pineda</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=Caospierre" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/scratchmex"><img src="https://avatars3.githubusercontent.com/u/4014888?v=4" width="100px;" alt=""/><br /><sub><b>Ivan Gonzalez</b></sub></a><br /><a href="https://github.com/DataScienceResearchPeru/covid-19_latinoamerica/commits?author=scratchmex" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

<!-- LICENSE -->

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Latin America Covid-19 Data Repository</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Data Science Research Peru</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
