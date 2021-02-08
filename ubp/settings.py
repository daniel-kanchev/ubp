BOT_NAME = 'ubp'
SPIDER_MODULES = ['ubp.spiders']
NEWSPIDER_MODULE = 'ubp.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
ITEM_PIPELINES = {
   'ubp.pipelines.DatabasePipeline': 300,
}
