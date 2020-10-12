# <img src="https://user-images.githubusercontent.com/32339251/95760847-2265f880-0cc9-11eb-8cd5-ca641cea0771.png" alt="" width="40" > Reactonite | v1.0

Reactonite is a free and open source wrapper for react which lets a person write vanilla html code and convert it to a react code easily, hence building a PWA, SPA.

## SDOS | Group 3

- Amogh Gulati
- Aniket Pradhan
- Avi Garg
- Chirag Jain

## Table of Contents

- [Introduction](#1.-introduction)
  - [Purpose](#1.1.-purpose)
  - [Background](#1.2.-background)
  - [Intended Audience](#1.3.-intended-audience)
  - [Project Scope](#1.4.-project-scope)
  - [Glossary](#1.5.-glossary)
  - [Abbreviations](#1.6.-abbreviations)
- [System Description](#2.-system-description)
  - [Product Features](#2.1.-product-features)
  - [Operating Environment](#2.2.-operating-environment)
  - [Functional Requirements](#2.3.-functional-requirements)
    - [High Priority](#2.3.1.-high-priority)
    - [Medium Priority](#2.3.2.-medium-priority)
    - [Low Priority](#2.3.3.-low-priority)

## 1. Introduction

### 1.1. Purpose

This is a Requirements Specification document for Reactonite. Reactonite is a free and open source wrapper for react which lets a person write vanilla HTML code and convert it to a react code easily, hence building a PWA, SPA. The main aim of Reactonite is to create a starter single page React app based on a HTML file made by the user.

### 1.2. Background

According to the [latest surveys](https://clutch.co/web-developers/resources/how-much-costs-build-website-2019), it can take anywhere from 50 to 100 hours to develop an initial landing page using the latest stack like [React](https://reactjs.org/), [Angular](https://angular.io/), etc. A nascent business or a corporate internal team might not need all the advanced features for their frontend which modern libraries like React provide but will benefit greatly by having a modern foundation in order to reduce technical debt later. We want developers with only the knowledge of HTML to be able to create an equivalent React app and experienced frontend developers to get boilerplate quickly so that it can reduce the number of man hours it takes to deliver the project.

### 1.3. Intended Audience

- Students
- Freelance Developers
- Early stage Entrepreneurs
- Backend Developers

### 1.4. Project Scope

The scope of this project is a command line based wrapper that takes a html file as an input from the user and provides an equivalent complete react project setup as an output. It further provides a command line interface to host the produced app on a local development server.

### 1.5. Glossary

|  **Term**   |                                                         **Definition **                                                          |
| :---------: | :------------------------------------------------------------------------------------------------------------------------------: |
|   Vanilla   |                                  Refers to using plain version/without any additional libraries                                  |
| Boilerplate | boilerplate code or just boilerplate are sections of code that have to be included in many places with little or no alteration.  |
|   Wrapper   |               A Wrapper is some code that is created to internally call some API without changing the actual API.                |
| Hot Reload  | Keeping the app running and injecting new versions of the files that you edited at runtime without losing the state information. |
|  Frontend   |                                 The frontend of a website is the part that users interact with.                                  |
|   Backend   |                                          The backend of a website consists of a server                                           |

### 1.6. Abbreviations

| **Word / Acronym** |    **Definition / Full Form**     |
| :----------------: | :-------------------------------: |
|        HTML        |     Hypertext Markup Language     |
|        PWA         |        Progressive Web App        |
|        SPA         |      Single Page Application      |
|         UI         |          User Interface           |
|         JS         |            javascript             |
|        API         | Application Programming Interface |

## 2. System Description

### 2.1. Product Features

- Create React applications as quickly as possible by typing minimal React code/components.
- Act as a “boilerplate” for React apps with basic UI.
- Allow props passing
- Hot Reloading
- Allow importing of already created Html file components
- Ability to import [reactstrap](https://reactstrap.github.io/), CSS libraries, [NPM](https://www.npmjs.com/) packages.
- API handler directly embedded into the system
- Responsive headers directly embedded into the system
- Access to react hooks
- Add vanilla CSS and JS
- Act as a wrapper to NPM

### 2.2. Operating Environment

1. A personal workstation for the user.
2. Requires the following software components to work
   1. Python
   2. NodeJS
   3. NPM
   4. A modern web browser that supports HTML5

### 2.3. Functional Requirements

#### 2.3.1. High Priority

- The system should produce valid single page react applications when given a valid HTML file as an input containing.
  - Fundamental tags.
  - Vanilla css
  - Vanilla js
- The system should allow importing of following files to enable component wise development as well as reusability of the code:
  - Other HTML files apart from entry point.
  - NPM packages (reactstrap and axios).
- Enable props passing for :
  - Style
  - Class
  - Form handlers
  - Event handlers
- The system should contain a file watcher (watchdog) which hot reloads the app (changing ui without building again).

#### 2.3.2. Medium Priority

- Contain a UI based mechanism to generate corresponding React code.
- The system should capture and present stdout and stdin streams while compilation during npm.
- Allow direct access to react hooks.
- Allow responsive headers to be added to the tags directory.
- Allow data fetching using API endpoints directly into the system.

#### 2.3.3. Low Priority

- Implement a mechanism for custom variables and code logic.
- System should add data and access mechanisms in HTML like states.
- Allow component wise hot reload.
