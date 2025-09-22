<div align= center>
	<h1>Masa Meter [beta]</h1>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://react.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![NGINX](https://img.shields.io/badge/NGINX-009639?style=flat&logo=nginx&logoColor=white)](https://nginx.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat&logo=gnu-bash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Cloudflare](https://img.shields.io/badge/Cloudflare-FF7800?style=flat&logo=cloudflare&logoColor=white)](https://www.cloudflare.com/)


</div>

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Architecure](#project-architecture)
- [Contributors](#contributors)
- [License](#license)

## Overview
Masa Meter is Python web application that integrates with a Discord bot and provides a web dashboard. The bot increments a counter whenever someone says "Sushi Masa", and the website displays:
- Current counter
- History of mentions
- Leaderboard ranking
- Achievements
- Random sushi picture (from Pexels API)

This project demonstrates modern full-stack development with Python, FastAPI, Discord.py, HTML, CSS, TypeScript, React, SQLite3, NGINX, Docker, and Cloudflare tunneling.

## Features
- Interactive Discord bot that tracks mentions of "Sushi Masa" (manual)
- React web interface showing counter, history, leaderboard, achievements, and sushi picutres
- Integration with <a href="https://www.pexels.com/">Pexels</a> photo API
- Lightweight SQLite3 database
- NGINX reverse proxy
- Docker containerization and deployment
- Cloudflare Tunneling for secure public access from personal Raspberry Pi

## Technologies Used
- **Python 3.11** – Core language  
- **SQLite3** – Database  
- **FastAPI** – Web framework
- **Discord.py** – Discord bot framework
- **React** – Frontend 
- **Pexels API** - Stock sushi pictures API
- **Docker** – Containerization and deployment
- **Cloudflare Tunnel** – Expose local server securely to the public

## Project Architecture
![Project Architecure](docs/architecture.png)

## Contributors
<table>
  <tr>
    <th>Contributor</th>
    <th>Role</th>
    <th>GitHub</th>
  </tr>
  <tr>
    <td align="center"><img src="https://github.com/yellowcrystalz.png" width="100" height="100"/></td>
    <td align="center">Lead Developer</td>
    <td align="center"><a href="https://github.com/yellowcrystalz">@Yellowcrystalz</a></td>
  </tr>
  <tr>
    <td align="center"><img src="https://github.com/dann-do.png" width="100" height="100"/></td>
    <td align="center">Developer</td>
    <td align="center"><a href="https://github.com/dann-do">@dann-do</a></td>
  </tr>
  <tr>
    <td align="center"><img src="https://github.com/RyujinKanao.png" width="100" height="100"/></td>
    <td align="center">Artist</td>
    <td align="center"><a href="https://github.com/RyujinKanao">@RyujinKanao</a></td>
  </tr>
  <tr>
    <td align="center"><img src="https://github.com/GracefulTania.png" width="100" height="100"/></td>
    <td align="center">Web Designer</td>
    <td align="center"><a href="https://github.com/GracefulTania">@GracefulTania</a></td>
  </tr>
</table>

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.