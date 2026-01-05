import requests

url = "https://stage.sxalable.io/query"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk4OGQ1YTM3OWI3OGJkZjFlNTBhNDA5MTEzZjJiMGM3NWU0NTJlNDciLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTWFkaHVUaGlydHlUd28gIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3N4YWxhYmxlLWRldiIsImF1ZCI6InN4YWxhYmxlLWRldiIsImF1dGhfdGltZSI6MTc2NjQ4MzgwMCwidXNlcl9pZCI6IkI3a2hCN0xKV0ljT1lZbDViSlgxeFZSOFJtUzIiLCJzdWIiOiJCN2toQjdMSldJY09ZWWw1YkpYMXhWUjhSbVMyIiwiaWF0IjoxNzY3MDA4NDA2LCJleHAiOjE3NjcwMTIwMDYsImVtYWlsIjoibWFkaHUuc3JpZGhhcmFuKzMyQHZlbHRyaXMuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm1hZGh1LnNyaWRoYXJhbiszMkB2ZWx0cmlzLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIiwidGVuYW50IjoibWFkaHV2ZWx0cmlzcWEzMi1rZHhnYyJ9fQ.hDWNVhsFFEp3VBPdB8K-jYsU20O8f0eFdI4Q_CLytpc_ULeMhcsV0hCMuVX766vDiIiogxUYnOYs85eu3gplj8_-hIS_DIxEOS810GSn8K0gWnGu8cBJfl2yDFl-q0nx4nksUukf8qYVxSfQ9fh9jwB7Weyzj0v4QK-263Wm3L-I7ovKHjigVXxky9RZPiUAAa726zTit0GYaGaplwN3vhyzIfi36UCXstbOBzOOxTtO7joDu8h41IoBB82BDKqC011tq5q3vE2MmhLrwuOI6xqyODSuis9PkszDtZod3QeshHu6IdWoT0br3hm4yO3Ta_vh6Et5L6IRyD8F4OHnxg"
}

mutation = """
mutation RouterStartStop {
    routerStartStop(
        licenseId: "ReleaseGCP_Veltris032",  #Router's license id
        operation: true # user true to start router
    ) {
        id
        name
        status
        serviceStatus
        deploymentStatus
        jwt
        licenseId
        deploymentType
        wanIP
        routerState
        publicIP
        isIpv6Enabled
        deploymentMode
        isConfigured
        gcpCredentials
        firewallRules
    }
}
"""

payload = {
    "query": mutation
}

response = requests.post(url, headers=headers, json=payload)

print("HTTP Status:", response.status_code)

# Pretty print JSON response
try:
    print("Response:")
    print(response.json())
except ValueError:
    print("Raw response:")
    print(response.text)
