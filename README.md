# CoCo-dataset-size-conversion-coco-
We made a program that can convert the COCO dataset to any size. Information of the annotations was also converted, not just the size.

main函数中给出对应的文件路径，确定无误后即可运行程序

请注意：
输出的annotation文件是在原来的annotation文件上添加新的转换后的信息而来的，即现在得到的annotation文件有双倍的images和annotations描述信息（一个是原来尺寸的，一个是转换后尺寸）
根据需要您可以手动删除不需要的信息，即删除以前的images和annotations描述信息，这花不了您多少时间。

我们根据自己实验的需要，只对annotation描述信息中的bbox做了对应尺度变换的更改，若您有需要，想更改annotation文件的其它信息，可以仿照我的写法自行更改。

另外，我们还写了一个验证程序val.py。他能画出bbox位置，以此来判断您是否转换正确。
