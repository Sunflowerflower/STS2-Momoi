using STS2_Momoi.Settings;

namespace STS2_Momoi.Diagnostics;

/// <summary>
/// 排查用详细日志（设置 → 诊断 →「输出详细日志」，默认关闭）。
///
/// 出牌动画、活力/火力消耗这些热路径上原来是无条件写 godot.log 的：一张牌要写 4~6 行，
/// 每行都是一次同步磁盘写入，牌多的时候就是肉眼可见的卡顿。现在统一走这里，只在开关打开时输出。
/// 调用点请写成 <c>if (MomoiDiag.Enabled) { MomoiDiag.Log($"…"); }</c>，
/// 这样开关关着时连字符串插值都不会发生。
/// </summary>
public static class MomoiDiag
{
    /// <summary>是否输出详细日志（读设置，本身开销很小）。</summary>
    public static bool Enabled => MomoiSettingsStore.VerboseLogging.Read();

    public static void Log(string message)
    {
        if (Enabled)
        {
            Entry.Logger.Info(message);
        }
    }

    public static void Warn(string message)
    {
        if (Enabled)
        {
            Entry.Logger.Warn(message);
        }
    }
}
