---
layout: page
permalink: /publications/
title: publications
description: Peer-reviewed publications by Sushil Awale on multimodal information retrieval, vision-language models, patent search, cultural heritage and scholarly knowledge graphs.
years: [2026, 2025, 2023, 2022]
nav: true
nav_order: 1
---
<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
