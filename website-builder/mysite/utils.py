def tenant_key_prefix(tenant):
    return f"tenant:{tenant.id}"

def website_list_cache_key(tenant):
    return f"{tenant_key_prefix(tenant)}:websites"

def website_cache_key(tenant, website_id):
    return f"{tenant_key_prefix(tenant)}:website:{website_id}"

def default_website_cache_key(tenant):
    return f"{tenant_key_prefix(tenant)}:default-website"
