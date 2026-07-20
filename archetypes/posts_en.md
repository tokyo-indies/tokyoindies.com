---
title: {{ (now.AddDate 0 1 0).Format "January 2006" }} Tokyo Indies
date: {{ .Date }}
draft: false

---

The next Tokyo Indies will be held on {{- $nextDate := "" -}}
{{- range seq 1 31 -}}
  {{- if eq $nextDate "" -}}
    {{- $checkDate := now.AddDate 0 0 . -}}
    {{- if and (eq (int $checkDate.Weekday) 3) (ge $checkDate.Day 15) (le $checkDate.Day 21) -}}
      {{- $nextDate = $checkDate.Format "January 2" -}}
    {{- end -}}
  {{- end -}}
{{- end -}}{{ print " " $nextDate }}.

We're accepting presentations on the [presentation page](/en/present).
