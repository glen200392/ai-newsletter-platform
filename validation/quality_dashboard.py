"""
CEO Newsletter 品質儀表板
實時監控 Newsletter 品質指標並提供可視化報告
"""

import json
from datetime import datetime
from pathlib import Path

def load_quality_data():
    """載入品質評估數據"""
    try:
        with open('data/task_tsk_0698/quality_assessment.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  找不到品質評估數據文件")
        return None

def generate_dashboard():
    """生成品質儀表板"""
    
    quality_data = load_quality_data()
    if not quality_data:
        return
    
    # 計算總體統計
    themes = list(quality_data.keys())
    total_score_avg = sum(q['total_score'] for q in quality_data.values()) / len(quality_data)
    
    completeness_avg = sum(q['completeness_score'] for q in quality_data.values()) / len(quality_data)
    data_avg = sum(q['data_score'] for q in quality_data.values()) / len(quality_data)
    ceo_avg = sum(q['ceo_perspective_score'] for q in quality_data.values()) / len(quality_data)
    readability_avg = sum(q['readability_score'] for q in quality_data.values()) / len(quality_data)
    structure_avg = sum(q['structure_score'] for q in quality_data.values()) / len(quality_data)
    
    print("=" * 100)
    print(" " * 30 + "📊 CEO NEWSLETTER 品質儀表板")
    print("=" * 100)
    print(f"更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"評估主題數: {len(quality_data)}")
    print("=" * 100)
    
    # 總體健康度指標
    print("\n🎯 總體健康度指標")
    print("-" * 100)
    
    # 計算健康度等級
    if total_score_avg >= 4.3:
        health_status = "優秀"
        health_icon = "✨"
        health_color = "綠"
    elif total_score_avg >= 4.0:
        health_status = "良好"
        health_icon = "✅"
        health_color = "淺綠"
    elif total_score_avg >= 3.5:
        health_status = "尚可"
        health_icon = "⚠️"
        health_color = "黃"
    else:
        health_status = "待改進"
        health_icon = "❌"
        health_color = "紅"
    
    print(f"\n當前狀態: {health_icon} {health_status} ({health_color}燈)")
    print(f"總體評分: {total_score_avg:.2f}/5.0")
    print(f"達標進度: {(total_score_avg / 4.3 * 100):.1f}% (目標: 4.3)")
    print(f"距離目標: {max(0, 4.3 - total_score_avg):.2f} 分")
    
    # 五維雷達圖數據
    print("\n📐 五維品質分析")
    print("-" * 100)
    
    def print_bar(label, score, target=4.0, width=40):
        """打印進度條"""
        filled = int((score / 5.0) * width)
        bar = "█" * filled + "░" * (width - filled)
        status = "✅" if score >= target else "⚠️" if score >= target - 0.5 else "❌"
        print(f"{label:20} {status} [{bar}] {score:.2f}/5.0 (目標: {target:.1f})")
    
    print_bar("完整性", completeness_avg, 4.5)
    print_bar("數據支持", data_avg, 4.5)
    print_bar("CEO 視角", ceo_avg, 4.0)
    print_bar("可讀性", readability_avg, 4.2)
    print_bar("結構品質", structure_avg, 5.0)
    
    # 各主題詳細評分
    print("\n📰 各主題詳細評分")
    print("-" * 100)
    print(f"{'主題':<35} {'總分':<12} {'完整性':<10} {'數據':<10} {'CEO':<10} {'可讀性':<10} {'結構':<10}")
    print("-" * 100)
    
    # 排序：最高分到最低分
    sorted_themes = sorted(quality_data.items(), key=lambda x: x[1]['total_score'], reverse=True)
    
    for key, data in sorted_themes:
        theme_name = data['theme']
        total = data['total_score']
        comp = data['completeness_score']
        data_s = data['data_score']
        ceo = data['ceo_perspective_score']
        read = data['readability_score']
        struct = data['structure_score']
        
        # 狀態圖標
        if total >= 4.3:
            icon = "✨"
        elif total >= 4.0:
            icon = "✅"
        elif total >= 3.5:
            icon = "⚠️"
        else:
            icon = "❌"
        
        print(f"{icon} {theme_name:<32} {total:>5.2f}/5.0   "
              f"{comp:>5.2f}/5.0  {data_s:>5.2f}/5.0  {ceo:>5.2f}/5.0  "
              f"{read:>5.2f}/5.0  {struct:>5.2f}/5.0")
    
    # 關鍵問題識別
    print("\n🚨 關鍵問題識別")
    print("-" * 100)
    
    critical_issues = []
    warnings = []
    
    for key, data in quality_data.items():
        theme = data['theme']
        
        # P0 問題：嚴重低於標準
        if data['ceo_perspective_score'] < 2.5:
            critical_issues.append(f"❌ {theme}: CEO 視角嚴重不足 ({data['ceo_perspective_score']:.1f}/5.0)")
        if data['total_score'] < 3.5:
            critical_issues.append(f"❌ {theme}: 總分過低，不建議發布 ({data['total_score']:.2f}/5.0)")
        
        # P1 問題：接近但未達標
        if 2.5 <= data['ceo_perspective_score'] < 4.0:
            warnings.append(f"⚠️  {theme}: CEO 視角需加強 ({data['ceo_perspective_score']:.1f}/5.0)")
        if 3.5 <= data['readability_score'] < 4.2:
            warnings.append(f"⚠️  {theme}: 可讀性待提升 ({data['readability_score']:.1f}/5.0)")
        if 4.0 <= data['data_score'] < 4.5:
            warnings.append(f"⚠️  {theme}: 數據支持可再補強 ({data['data_score']:.1f}/5.0)")
    
    if critical_issues:
        print("\n🔴 P0 級問題（必須立即解決）:")
        for issue in critical_issues:
            print(f"  {issue}")
    else:
        print("\n✅ 無 P0 級嚴重問題")
    
    if warnings:
        print("\n🟡 P1 級警告（應盡快改進）:")
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("\n✅ 無 P1 級警告")
    
    # 優勢分析
    print("\n💎 優勢與亮點")
    print("-" * 100)
    
    strengths = []
    for key, data in quality_data.items():
        theme = data['theme']
        if data['structure_score'] >= 5.0:
            strengths.append(f"✨ {theme}: 結構品質完美")
        if data['data_score'] >= 4.8:
            strengths.append(f"✨ {theme}: 數據支持極佳")
        if data['completeness_score'] >= 4.8:
            strengths.append(f"✨ {theme}: 內容完整性優秀")
    
    if strengths:
        for strength in strengths:
            print(f"  {strength}")
    else:
        print("  暫無明顯優勢項目")
    
    # 改進優先順序建議
    print("\n🎯 改進優先順序")
    print("-" * 100)
    
    print("\n優先級 P0 (本週完成):")
    print("  1. 提升 CEO 視角適配度 (當前: {:.1f}/5.0 → 目標: 4.0+)".format(ceo_avg))
    print("     - 添加 CEO 決策框架段落")
    print("     - 增強可操作建議密度")
    print("     - 預計工作量: 8 小時")
    
    print("\n優先級 P1 (下週完成):")
    print("  2. 優化可讀性 (當前: {:.1f}/5.0 → 目標: 4.2+)".format(readability_avg))
    print("     - 段落合併與擴展")
    print("     - 減少列表，增加敘事")
    print("     - 預計工作量: 6 小時")
    
    print("  3. 補強數據來源 (當前: {:.1f}/5.0 → 目標: 4.5+)".format(data_avg))
    print("     - 確保每篇 ≥4 個來源引用")
    print("     - 多樣化來源類型")
    print("     - 預計工作量: 3 小時")
    
    # 預測改進效果
    print("\n📈 預測改進效果")
    print("-" * 100)
    
    # 假設完成 P0 + P1 改進
    predicted_ceo = min(4.2, ceo_avg + 2.0)
    predicted_read = min(4.6, readability_avg + 0.8)
    predicted_data = min(4.8, data_avg + 0.4)
    
    predicted_total = (
        completeness_avg * 0.20 +
        predicted_data * 0.25 +
        predicted_ceo * 0.25 +
        predicted_read * 0.15 +
        structure_avg * 0.15
    )
    
    improvement = predicted_total - total_score_avg
    
    print(f"\n完成所有優化後預測:")
    print(f"  當前總分: {total_score_avg:.2f}/5.0")
    print(f"  預測總分: {predicted_total:.2f}/5.0")
    print(f"  預期提升: +{improvement:.2f} 分 ({improvement/total_score_avg*100:.1f}%)")
    print(f"  達標狀態: {'✅ 達理想標準 (4.3+)' if predicted_total >= 4.3 else '✅ 達最低標準 (4.0+)' if predicted_total >= 4.0 else '⚠️  仍需繼續優化'}")
    
    # 時間軸與里程碑
    print("\n⏰ 優化時間軸")
    print("-" * 100)
    
    print("\n本週 (2026-02-04 ~ 02-10):")
    print("  ✓ 完成品質評估")
    print("  ✓ 完成優化建議")
    print("  ⏳ 執行 P0 優化")
    print("  ⏳ 重新評估品質")
    
    print("\n下週 (2026-02-11 ~ 02-17):")
    print("  ⏳ 執行 P1 優化")
    print("  ⏳ 外部 CEO 測試 (5-10 人)")
    print("  ⏳ 收集反饋")
    
    print("\n第三週 (2026-02-18 ~ 02-24):")
    print("  ⏳ 最終迭代")
    print("  ⏳ 準備發布材料")
    print("  🎯 正式上線")
    
    # 關鍵指標追蹤
    print("\n📊 關鍵指標追蹤 (KPIs)")
    print("-" * 100)
    
    print(f"\n{'指標':<25} {'當前值':<15} {'目標值':<15} {'達標率':<15} {'狀態'}")
    print("-" * 100)
    
    kpis = [
        ("總體評分", total_score_avg, 4.3, total_score_avg / 4.3 * 100),
        ("CEO 視角評分", ceo_avg, 4.0, ceo_avg / 4.0 * 100),
        ("可讀性評分", readability_avg, 4.2, readability_avg / 4.2 * 100),
        ("數據支持評分", data_avg, 4.5, data_avg / 4.5 * 100),
        ("完整性評分", completeness_avg, 4.5, completeness_avg / 4.5 * 100),
    ]
    
    for name, current, target, percentage in kpis:
        status = "✅" if percentage >= 100 else "🟡" if percentage >= 90 else "🔴"
        print(f"{name:<25} {current:>6.2f}/5.0     {target:>6.1f}/5.0     {percentage:>6.1f}%        {status}")
    
    # 儀表板總結
    print("\n" + "=" * 100)
    print("📌 儀表板總結")
    print("=" * 100)
    
    if total_score_avg >= 4.3:
        summary = "🎉 Newsletter 品質優秀，已達理想發布標準！建議立即推向市場。"
    elif total_score_avg >= 4.0:
        summary = "✅ Newsletter 品質良好，達最低可發布標準。建議執行外部測試後發布。"
    elif total_score_avg >= 3.5:
        summary = "⚠️  Newsletter 品質尚可，需要改進後發布。建議完成 P0 優化再評估。"
    else:
        summary = "❌ Newsletter 品質待改進，不建議當前發布。需大幅優化。"
    
    print(f"\n{summary}")
    
    print(f"\n下一步行動:")
    if total_score_avg < 4.0:
        print("  1. 執行 P0 優化（CEO 視角）")
        print("  2. 重新生成 Newsletter")
        print("  3. 再次評估品質")
    elif total_score_avg < 4.3:
        print("  1. 執行 P1 優化（可讀性、數據）")
        print("  2. 邀請 CEO 試讀")
        print("  3. 根據反饋調整")
    else:
        print("  1. 準備發布材料")
        print("  2. 設計訂閱頁面")
        print("  3. 啟動市場推廣")
    
    print("\n" + "=" * 100)
    print("儀表板生成完成 | 數據更新於 " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 100 + "\n")

if __name__ == "__main__":
    generate_dashboard()
