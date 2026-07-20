---
title: {{ (now.AddDate 0 1 0).Year }}年{{ (now.AddDate 0 1 0).Month | int }}月のTokyo Indies～REPLACETHEME特集
date: {{ .Date }}
draft: false
featured_image: "img/TODO:.png"
images: ["img/TODO:.png"]
---

次のTokyo Indiesは{{- $nextDay := "" -}}{{- $nextMonth := "" -}}
{{- range seq 1 31 -}}
  {{- if eq $nextDay "" -}}
    {{- $checkDate := now.AddDate 0 0 . -}}
    {{- if and (eq (int $checkDate.Weekday) 3) (ge $checkDate.Day 15) (le $checkDate.Day 21) -}}
      {{- $nextMonth = $checkDate.Month | int -}}
      {{- $nextDay = $checkDate.Day | int -}}
    {{- end -}}
  {{- end -}}
{{- end -}}{{ print $nextMonth "月" $nextDay "日" }}開催です。

今月はREPLACETHEME特集です！

![](/img/TODO:.png)

プレゼンを募集しています。詳細については[プレゼン申込みページ](/present)をご確認ください。
