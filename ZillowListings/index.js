import fetch from 'node-fetch'
import * as cheerio from 'cheerio'
import fs from 'fs'
import { Parser } from '@json2csv/plainjs';

(async () => {

    let finalJsonArray = []

    for (let i = 0; i < 10; i++) {
        const urlParams = `{"pagination":{"currentPage":${i + 1}}}`
        const encodedUrl = "https://www.zillow.com/san-diego-ca/2_p/?searchQueryState=" + encodeURIComponent(urlParams)

        const response = await fetch(encodedUrl, {
            headers: {
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,no;q=0.6,nn;q=0.5",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "Referrer-Policy": "unsafe-url"
            }
        })

        const text = await response.text()
        const $ = cheerio.load(text)

        let script = $('#__NEXT_DATA__')
        if(script.length == 0) script = $("#wrapper > script:nth-child(9)")

        const json = JSON.parse(script.text().replaceAll("<!--", "").replaceAll("-->", ""))

        if(json.cat1)
            finalJsonArray = finalJsonArray.concat(json.cat1.searchResults.listResults)
        else 
            finalJsonArray = finalJsonArray.concat(json.props.pageProps.searchPageState.cat1.searchResults.listResults)
    }


    const csv = new Parser().parse(finalJsonArray);
    fs.writeFileSync("csv.csv", csv)

})()