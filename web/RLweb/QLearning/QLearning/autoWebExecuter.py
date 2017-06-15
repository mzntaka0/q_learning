from selenium import webdriver


if __name__ == '__main__':
    dim_list = [i for i in range(5, 101, 5)]
    for i in dim_list:
        browser = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        browser.get('http://127.0.0.1:8000')

        element = browser.find_element_by_name('file')
        element.send_keys('/Users/mzntaka0/Work/9DW/IYO/reinforcement_learning/web/RLweb/test_jsons/params_dim_{}.json'.format(i))

        submit = browser.find_element_by_xpath("//*[@type='submit']")
        submit.submit()

        browser.close()
