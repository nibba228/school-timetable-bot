from sys import stdout


config = {
    'handlers': [
        {
            'sink': stdout, 
            'format': '[<green>{time:DD MMM YYYY}</green> | <green>{time:HH:mm:ss}</green>] <lvl>{level}</lvl> in <blue>{file}</blue> function <magenta>{function}</magenta> line <yellow>{line}</yellow> <fg 76,17,145>::</fg 76,17,145> <lvl>{message}</lvl>',
            'diagnose': False,
        },

        {
            'sink': 'logs\log.log',
            'format': '[<green>{time:DD MMM YYYY}</green> | <green>{time:HH:mm:ss}</green>] <lvl>{level}</lvl> in <blue>{file}</blue> function <magenta>{function}</magenta> line <yellow>{line}</yellow> <fg 76,17,145>::</fg 76,17,145> <lvl>{message}</lvl>',
            'rotation': '1 MB',
            'compression': 'zip',
            'encoding': 'utf-8'
        }
    ]
}