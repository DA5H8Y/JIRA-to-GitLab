external_url 'https://gitlab.internal'
gitlab_rails['initial_root_password'] = File.read('/run/secrets/gitlab_root_password').gsub("\n", "")
gitlab_rails['omniauth_enabled'] = true
gitlab_rails['omniauth_allow_single_sign_on'] = ['kerberos']

gitlab_rails['kerberos_enabled'] = true
gitlab_rails['kerberos_keytab'] = '/etc/gitlab/http.keytab'

# This needs to be set to allow ticket based authentication.
gitlab_rails['kerberos_use_dedicated_port'] = true
gitlab_rails['kerberos_port'] = 8443
# HTTPS will be disabled here because NGINX cares about 
# routing its incomming TLS encrypted kerberos requests
# over HTTP docker-internaly to GitLab.
gitlab_rails['kerberos_https'] = false