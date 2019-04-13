<p align="center">
  <a href="https://github.com/wenyalintw/Dicom_Viewer">
    <img src="https://i.imgur.com/Uid1O3A.png" alt="Dicom Viewer" width="96" height="96">
  </a>
  <h2 align="center">簡易醫學影像GUI (Dicom Viewer)</h2>
  <p align="center">能顯示 2D/3D Dicom影像的應用</p>
  <br>
</p>

本project旨在利用python+Qt製作簡易的醫學影像GUI，提供一個平台，能在上面使用python開發測試各式影像處理功能，尤其是針對3D之Dicom Stack

## 先看兩段Demo吧！
  <a href="#">
    2D Image Processing
  </a>
  <br>
  <a href="#">
    3D Image Processing
  </a>
  
<!---
<sub>看看我的[部落格](http://kamranahmed.info)，然後來 [Twitter](https://twitter.com/kamranahmedse) 說聲 "hi"。</sub><br>
<sub>（譯註：也歡迎來逛逛譯者的[部落格](http://goodjack.blogspot.com/)，然後來 [Twitter](https://twitter.com/littlegoodjack) 打個招呼 :P）</sub>
-->

## 執行畫面
執行程式會打開Main Window，左上角的選單有2D processing和3D processing兩個子選項，其中後者embed有3D volume reconstruction功能


### 2D processing
內含功能
- Load Image (含*.dcm)
- Save Image
- Convert to gray scale
- Restore
- Thresholding
- Region Growing
- Morthology (Dilation, Erosion, Opening, Closing)
- Edge Detection (Laplacian, Sobel, Perwitt, Frei & Chen)
- Drawing
<br>
<a href="https://github.com/wenyalintw/Dicom_Viewer">
    <img src="resources/2D_Processing.jpg" alt="2D_Processing" width="960" height="480">
</a>


### 3D processing
內含功能
- Load DICOM stack
- Save slice (axial, sagittal, coronal)
- Colormap transform
- Slider scrolling
- Mouse hovering/clicking
- Show DICOM info
- Show slice index coordinate
- 3D volume reconstruction
<br>
<a href="https://github.com/wenyalintw/Dicom_Viewer">
    <img src="resources/3D_Processing.jpg" alt="3D_Processing" width="960" height="480">
</a>

### 3D volume reconstruction
<br>
<a href="https://github.com/wenyalintw/Dicom_Viewer">
    <img src="resources/3D_Volume.jpg" alt="3D_Volume" width="960" height="480">
</a>

* 更新 Sponsored By 段落

### 譯者前言
嗨大家好我是小克 👋，從 2017 年開始注意到這個 repo 覺得獲益良多，所以就試著翻譯看看，分享給更多需要的人。由於這裡是翻譯 repo，關於內容的任何建議，推薦你直接回饋給 [kamranahmedse/developer-roadmap](https://github.com/kamranahmedse/developer-roadmap)，當然需要我協助也是可以的 :D

這裡的中文都盡量使用 **台灣用語及術語**，資訊相關的術語都會在翻譯旁保留原文供參考。中文排版皆盡可能地依循 [**中文文案排版指北**](https://github.com/sparanoid/chinese-copywriting-guidelines)（若有不符的地方請跟我說）。

這是我第一次翻譯，難免有疏漏、語意不順、用詞不精準及翻譯錯誤的地方，如果有任何可以改進之處，都非常歡迎開 issue 或 PR！

當然，若原作有更新，也歡迎開 issue 告知，或 PR 協助翻譯，謝謝！

接受任何意見回饋 [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/littlegoodjack.svg?style=social&label=Follow%20@littlegoodjack)](https://twitter.com/littlegoodjack)

> <sub>小小的推廣拙作：[小克的 Visual Studio Code 必裝擴充套件（Extensions）私藏推薦](http://goodjack.blogspot.com/2018/03/visual-studio-code-extensions.html)</sub>

## 免責聲明
> 這些路線圖的目的是給你一個輪廓，並在你困惑接下來該學什麼的時候指導你。而不是鼓勵你學習很潮很流行的東西。你應該要更加了解，為什麼某個工具會比其他的工具更適合用在一些情況，並記住潮和流行，從來就不代表它是最適合完成任務的工具。

## 介紹

![Web 開發人員路線圖介紹](./chinese-version/images/intro.png)

## 前端 Frontend 路線圖

![前端 Frontend 路線圖](./chinese-version/images/frontend.png)

## 後端 Back-end 路線圖

![後端 Back-end 路線圖](./chinese-version/images/backend.png)

## DevOps 路線圖

![DevOps 路線圖](./chinese-version/images/devops.png)

## 🚦 總結

如果你認為路線圖有可以改進的地方，請更新並開個 PR 或是送出 issue。另外，我也會繼續改進這個專案，所以你可能會想要 watch 或 star 這個專案以便再來觀看。

## 🙌 貢獻

> 到 [貢獻文件](./contributing.md) 看看怎麼更新這些路線圖

- 改進並開啟 Pull Request
- 在 Issue 中討論想法
- 分享出去
- 接受任何意見回饋 [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/kamranahmedse.svg?style=social&label=Follow%20%40kamranahmedse)](https://twitter.com/kamranahmedse)
- （關於中文翻譯）接受任何意見回饋 [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/littlegoodjack.svg?style=social&label=Follow%20@littlegoodjack)](https://twitter.com/littlegoodjack)

## Sponsored By

- [**Hackr.io** - Best Online Programming Courses & Tutorials Recommended by the Programming Community](https://hackr.io)
- [**Educative.io**: Become an employable Web Developer from scratch with this interactive learning track. Try a free preview today!](https://www.educative.io/track/beginning-front-end-developer)
