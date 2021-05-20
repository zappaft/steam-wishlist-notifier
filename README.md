<!--
*** template by https://github.com/othneildrew/Best-README-Template
-->

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Steam wishlist notifier</h3>
  <p align="center">
    Get your game sales, without needing to check steam's page.
    Without doing anything at all.
    <br />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Due to my own experience of constantly checking steam sales every day...
I decided to try and build something to automate it.

### Built With

* [Python 3.9](https://www.python.org/downloads/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

You need [Python](https://www.python.org/downloads/). Chances are that it's only 3.9
compatible due to typehints, but it may work between 3.6 and 3.8

I would recommend you to install virtualenv before you processed on pip installs.
(It may be installed by default)

* Virtualenv
  ```sh
  pip install venv
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/zappaft/steam-wishlist-notifier.git
   ```
2. Create a virtualenv
   ```sh
    python -m virtualenv venv
    ```
3. Initialize virtualenv
   ```sh
    \venv\Scripts\activate.bat
    ```
4. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
## Usage

You can now simply run the main script, and it will keep pushing notifications to your
desktop.
1. Run
   ```sh
   python main.pyw
   ```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Felipe Rocha - feliperch94@gmail.com

Project Link: [https://github.com/zappaft/steam-wishlist-notifier](https://github.com/zappaft/steam-wishlist-notifier)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username