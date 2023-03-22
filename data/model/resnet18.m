Network torchvision.models.resnet {
Layer Conv2d-1 {
Type: CONV
Stride { X: 2, Y: 2 }
Dimensions { K: 64, C: 3, R: 7, S: 7, Y: 224, X: 224 }
}
Layer Conv2d-2 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 64, C: 64, R: 3, S: 3, Y: 56, X: 56 }
}
Layer Conv2d-3 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 64, C: 64, R: 3, S: 3, Y: 56, X: 56 }
}
Layer Conv2d-4 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 64, C: 64, R: 3, S: 3, Y: 56, X: 56 }
}
Layer Conv2d-5 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 64, C: 64, R: 3, S: 3, Y: 56, X: 56 }
}
Layer Conv2d-6 {
Type: CONV
Stride { X: 2, Y: 2 }
Dimensions { K: 128, C: 64, R: 3, S: 3, Y: 56, X: 56 }
}
Layer Conv2d-7 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 128, C: 128, R: 3, S: 3, Y: 28, X: 28 }
}
Layer Conv2d-8 {
Type: CONV
Stride { X: 2, Y: 2 }
Dimensions { K: 128, C: 64, R: 1, S: 1, Y: 56, X: 56 }
}
Layer Conv2d-9 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 128, C: 128, R: 3, S: 3, Y: 28, X: 28 }
}
Layer Conv2d-10 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 128, C: 128, R: 3, S: 3, Y: 28, X: 28 }
}
Layer Conv2d-11 {
Type: CONV
Stride { X: 2, Y: 2 }
Dimensions { K: 256, C: 128, R: 3, S: 3, Y: 28, X: 28 }
}
Layer Conv2d-12 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 256, C: 256, R: 3, S: 3, Y: 14, X: 14 }
}
Layer Conv2d-13 {
Type: CONV
Stride { X: 2, Y: 2 }
Dimensions { K: 256, C: 128, R: 1, S: 1, Y: 28, X: 28 }
}
Layer Conv2d-14 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 256, C: 256, R: 3, S: 3, Y: 14, X: 14 }
}
Layer Conv2d-15 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 256, C: 256, R: 3, S: 3, Y: 14, X: 14 }
}
Layer Conv2d-16 {
Type: CONV
Stride { X: 2, Y: 2 }
Dimensions { K: 512, C: 256, R: 3, S: 3, Y: 14, X: 14 }
}
Layer Conv2d-17 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 512, C: 512, R: 3, S: 3, Y: 7, X: 7 }
}
Layer Conv2d-18 {
Type: CONV
Stride { X: 2, Y: 2 }
Dimensions { K: 512, C: 256, R: 1, S: 1, Y: 14, X: 14 }
}
Layer Conv2d-19 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 512, C: 512, R: 3, S: 3, Y: 7, X: 7 }
}
Layer Conv2d-20 {
Type: CONV
Stride { X: 1, Y: 1 }
Dimensions { K: 512, C: 512, R: 3, S: 3, Y: 7, X: 7 }
}
Layer Linear-21 {
Type: CONV
Dimensions { K: 1000, C: 512, R: 1, S: 1, Y: 1, X: 1 }
}
}