<div align="right">
  语言:
    🇨🇳
  <a title="英语" href="./README.en.md">🇺🇸</a>
  <!-- <a title="俄语" href="../ru/README.md">🇷🇺</a> -->
</div>

 <div align="center"><a title="" href="https://github.com/ZJCV/ZTransforms.git"><img align="center" src="./imgs/ZTransforms.png"></a></div>

<p align="center">
  «ZTransforms»是一个图像数据扩充代码库
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square"></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg"></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg"></a>
</p>

参考[pytorch/vision](https://github.com/pytorch/vision/)实现架构，以[imgaug](https://github.com/aleju/imgaug)为后端实现图像数据扩充。[imgaug](https://github.com/aleju/imgaug)支持的图像格式为`numpy ndarray`，数据类型默认为`uint8`，通道排列顺序为`RGB`。

## 内容列表

- [内容列表](#内容列表)
- [背景](#背景)
- [主要维护人员](#主要维护人员)
- [致谢](#致谢)
- [参与贡献方式](#参与贡献方式)
- [许可证](#许可证)

## 背景

[PyTorch](https://github.com/pytorch/pytorch)除了拥有强大的深度学习代码库之外，还额外提供了数据集处理、模型定义以及数据转换的实现[pytorch/vision](https://github.com/pytorch/vision/)。其中[transforms](https://github.com/pytorch/vision/tree/master/torchvision/transforms)模块默认以`PIL`为后端（*也可以使用更快的`Pillow-SIMD`，如果安装的话*）提供了多种数据转换功能，比如旋转、翻转、颜色抖动、随机裁剪、中心裁剪等等。不过随着深度学习的发展，越来越多的数据转换功能被发现，而`PIL`库并没有进行实现

在网上找到另一个数据扩充功能库[imgaug](https://github.com/aleju/imgaug)，其实现了更多的数据转换函数。所以新建这个代码库，参考[transforms](https://github.com/pytorch/vision/tree/master/torchvision/transforms)实现方式，以[imgaug](https://github.com/aleju/imgaug)为后端进行数据转换

## 主要维护人员

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## 致谢

* [pytorch/vision](https://github.com/pytorch/vision)
* [aleju/imgaug](https://github.com/aleju/imgaug)

```
@misc{imgaug,
  author = {Jung, Alexander B.
            and Wada, Kentaro
            and Crall, Jon
            and Tanaka, Satoshi
            and Graving, Jake
            and Reinders, Christoph
            and Yadav, Sarthak
            and Banerjee, Joy
            and Vecsei, Gábor
            and Kraft, Adam
            and Rui, Zheng
            and Borovec, Jirka
            and Vallentin, Christian
            and Zhydenko, Semen
            and Pfeiffer, Kilian
            and Cook, Ben
            and Fernández, Ismael
            and De Rainville, François-Michel
            and Weng, Chi-Hung
            and Ayala-Acevedo, Abner
            and Meudec, Raphael
            and Laporte, Matias
            and others},
  title = {{imgaug}},
  howpublished = {\url{https://github.com/aleju/imgaug}},
  year = {2020},
  note = {Online; accessed 01-Feb-2020}
}
```

## 参与贡献方式

欢迎任何人的参与！打开[issue](https://github.com/zjykzj/ZTransforms/issues)或提交合并请求。

注意:

* `GIT`提交，请遵守[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)规范
* 语义版本化，请遵守[Semantic Versioning 2.0.0](https://semver.org)规范
* `README`编写，请遵守[standard-readme](https://github.com/RichardLitt/standard-readme)规范

## 许可证

[Apache License 2.0](LICENSE) © 2021 zjykzj