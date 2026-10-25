# ERPNext-ը հայերենով

Frappe, ERPNext և Frappe HR համակարգերի 16-րդ տարբերակի հայերեն թարգմանությունը։ Սա փոքր Frappe հավելված է․ տեղադրում եք, լեզուն փոխում եք Հայերենի, և վերջ։

[English](README.md)

## Տեղադրում

Եթե արդեն ունեք ERPNext՝

```bash
cd frappe-bench
bench get-app https://github.com/nastaran-hasanloo/erpnext_armenian --branch version-16
bench --site your-site install-app erpnext_armenian
bench --site your-site clear-cache
```

Ձեր տվյալները չեն փոխվում, և ցանկացած պահի կարող եք հեռացնել հավելվածը։ Frappe Cloud-ի և Docker-ի համար տե՛ս [անգլերեն README-ն](README.md)։

## Ինչպես միացնել հայերենը

- Միայն ձեզ համար՝ My Settings > Language > Հայերեն, պահպանեք և թարմացրեք էջը։
- Բոլորի համար՝ System Settings > Language > Հայերեն։
- Նոր կայքում պարզապես ընտրեք Հայերեն կարգավորման ժամանակ։

Ամսաթվերը կլինեն `25.10.2026` ձևով, թվերը՝ `1 234,56`, իսկ շաբաթը կսկսվի երկուշաբթիից։

## Ուզում եք պարզապես փորձե՞լ

Պետք է միայն [Docker Desktop](https://www.docker.com/products/docker-desktop/)։

- Windows՝ ներբեռնեք ZIP-ը, բացեք և կրկնակի սեղմեք `docker/START-ERPNext-Armenian.bat`
- Linux կամ macOS՝ `./docker/erpnext-armenian.sh`

Առաջին անգամ մոտ 20-40 րոպե է տևում։ Հետո բացեք http://localhost:8080, մուտք՝ `Administrator` / `admin` (միայն փորձարկման համար)։

## Եթե ինչ-որ բան անգլերեն է մնացել

Գործարկեք `bench --site your-site clear-cache` և թարմացրեք էջը Ctrl+Shift+R-ով։ Եթե դեռ անգլերեն է, բացեք issue սքրինշոթով։

## Կարևոր է իմանալ

Առաջին տարբերակը արվել է թարգմանչական գործիքներով և մեկ միասնական բառարանով, հետո ձեռքով ստուգվել։ Որոշ արտահայտություններ, հատկապես հաշվապահական, կարող են անսովոր հնչել։ Եթե ինչ-որ բան սխալ կամ տարօրինակ է թվում, խնդրում ենք ուղղել կամ գրել մեզ։ Մանրամասները՝ [CONTRIBUTING.md](CONTRIBUTING.md)։

Սա միայն ինտերֆեյսի թարգմանություն է։ ԱԱՀ-ն, ՊԵԿ էլեկտրոնային հաշիվ-ապրանքագրերը, աշխատավարձը, ՀՀ հաշվային պլանը և բանկերը դեռ չկան։
