# 基于手机传感器的行为识别
本项目为服务器后端，安卓前端在 https://github.com/sqyon/CellPhoneActivityRecognitionAPP

使用安卓手机的传感器获取加速度与重力加速度，并计算出水平与垂直加速度，提取特征后使用决策树进行分类。
# 训练用数据集
https://github.com/mmalekzadeh/motion-sense
# 特征提取
使用tsfresh提取时间序列特征，使用卡方检验获取前k个最重要的特征，并使用这些特征进行训练
# 数据传输
手机端UPD发包到服务器进行计算输出，并回传手机
