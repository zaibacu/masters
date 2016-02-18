def pimp_my_selenium(driver):
    driver.set_preference("places.history.enabled", False)
    driver.set_preference("privacy.clearOnShutdown.offlineApps", True)
    driver.set_preference("privacy.clearOnShutdown.passwords", True)
    driver.set_preference("privacy.clearOnShutdown.siteSettings", True)
    driver.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
    driver.set_preference("signon.rememberSignons", False)
    driver.set_preference("network.cookie.lifetimePolicy", 2)
    driver.set_preference("network.dns.disablePrefetch", True)
    driver.set_preference("network.http.sendRefererHeader", 0)

    # set socks proxy
    driver.set_preference("network.proxy.type", 1)
    driver.set_preference("network.proxy.socks_version", 5)
    driver.set_preference("network.proxy.socks", '127.0.0.1')
    driver.set_preference("network.proxy.socks_port", 9030)
    driver.set_preference("network.proxy.socks_remote_dns", True)

    # if you're really hardcore about your security
    # js can be used to reveal your true i.p.
    # driver.set_preference( "javascript.enabled", False )

    # get a huge speed increase by not downloading images
    driver.set_preference("permissions.default.image", 2)