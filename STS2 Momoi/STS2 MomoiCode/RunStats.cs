namespace STS2_Momoi;

/// <summary>
/// 整局游戏（run）级共享状态：真理部 / C&C 的解锁进度等。
/// 由 Entry 订阅 RunManager.RunStarted 在每局开始时重置。
/// </summary>
public static class RunStats
{
    /// <summary>「来自真理部的协助」已选过的选项（3 个基础选项全部选过后解锁千寻）。</summary>
    public static readonly HashSet<string> VeritasPicked = new();

    /// <summary>「来自C&C的援护」已选过的选项（4 个基础选项全部选过后解锁时）。</summary>
    public static readonly HashSet<string> CnCPicked = new();

    /// <summary>「白与黑」的选择（整局游戏继承，null 表示尚未选择）。</summary>
    public static string? WhiteBlackChoice;

    public static void Reset()
    {
        VeritasPicked.Clear();
        CnCPicked.Clear();
        WhiteBlackChoice = null;
    }
}
