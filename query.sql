SELECT * 
FROM 
(SELECT T1.Company, T2.High_Stock_Price, T1.DateTime, T1.Hour
 FROM 
 (SELECT name AS Company, high, ts AS DateTime, SUBSTRING(ts, 12, 2) AS Hour FROM finance_stream_data) T1
INNER JOIN 
 (SELECT name, SUBSTRING(ts, 12, 2) AS hour, MAX(high) AS High_Stock_Price 
  FROM finance_stream_data
  GROUP BY name, SUBSTRING(ts, 12, 2)) T2
ON T1.Company = T2.name AND T1.high = T2.High_Stock_Price AND T1.Hour = T2.hour)
ORDER BY Company, Hour, DateTime
