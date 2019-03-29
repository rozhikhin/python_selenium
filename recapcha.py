from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

api_key = '3d6788ccf7b8ec387e76ff60898d00d8'
# site_key = '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'  # grab from site
site_key = '6LctgAgUAAAAACsC7CsLr_jgOWQ2ul2vC_ndi8o2'  # grab from site
url = 'https://www.google.com/recaptcha/api2/demo'

client = AnticaptchaClient(api_key)
task = NoCaptchaTaskProxylessTask(url, site_key)
job = client.createTask(task)
job.join()
response = job.get_solution_response()
print(response)

# driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response

# https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LctgAgUAAAAACsC7CsLr_jgOWQ2ul2vC_ndi8o2&co=aHR0cHM6Ly9ncm91cHMuZ29vZ2xlLmNvbTo0NDM.&hl=en&v=v1552285980763&size=normal&cb=v6bdwn24dw08

# 03AOLTBLTNtPFX4Os_dkzAZ3knLK34x5NGGZddx48XTpvGq5AXjBMBpHh5eWXL8mL5bd_oy1Y8EsI8tgiiCSYOjlkxp__HbmYCWv2j-pzh4doii_-V06UKUffsbANxwMC5Nu83H-OlprDK6AXZcRuAo_iPEyaYMOJYVB4s6sg2tLhYWaOxc8yaMVtqSSzoEcAVGFjh6oQ-mFP1m29aKzZQSjthCdPSAdCgUauMpkWsJhxibydFxcxV6Z81ZkOz8IMQq24OH4ZjKPFMkcDgyZaYLn-jaTGEQf0EqOI1lahGkOAAdf5wbe32gRM0yNL-rIAyOMhxjNpQTC2BW3W8sAm1CuIvOUph1lN81LuONcrdryxfPBaJaLJpSZuvUbA3fgHsmQizr6cleaug7-yS4atigh4eZAyLD2JUuKtCdJ4Jnib7EjJAfiBqylG9HGu47LQEwb-JVkC26C9X6SXD2D1BbU8WsSQY1PjOoA