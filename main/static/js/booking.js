document.addEventListener('DOMContentLoaded', () => {
  const calendar = document.querySelector('#calendar')
  const current_month = document.querySelector('#current_month')
  const next_month = document.querySelector('#next_month')
  const prev_month = document.querySelector('#prev_month')
  const scenario = document.querySelector('#scenario')
  const start_time = document.querySelector('#start_time')
  const participant = document.querySelector('#participant')
  const price = document.querySelector('#price')

  const notificationCard = document.querySelector('#notification-card')
  const notificationMsg = document.querySelector('#notification-message')

  const baseUrl = window.location.protocol + '//' + window.location.host + '/'

  const { pathname } = window.location
  const paths = pathname.split('/').filter((entry) => entry !== '')
  const lastPath = paths[paths.length - 1]

  let interval_timer

  let data

  let url

  next_month.addEventListener('click', function (e) {
    e.preventDefault()
    nextMonth()
  })
  prev_month.addEventListener('click', function (e) {
    e.preventDefault()
    prevMonth()
  })
  scenario.addEventListener('change', function (e) {
    e.preventDefault()
    changeScenarioInput()
  })
  participant.addEventListener('change', function (e) {
    e.preventDefault()
    changeParticipantInput()
  })

  /**
   * Chargement evmnt précédent mois
   */
  function prevMonth() {
    url = getUrl(calendar_date.getDate(), 'prev_month', lastPath)

    loadData(url).then((r) => {
      processData()
    })
  }

  /**
   * Chargement evmnt prochain mois
   */
  function nextMonth() {
    url = getUrl(calendar_date.getDate(), 'next_month', lastPath)

    loadData(url).then(() => {
      processData()
    })
  }

  /**
   * Retourne le nom du mois
   * @param monthNumber
   * @returns {string}
   */
  function getMonthName(monthNumber) {
    const date = new Date()
    date.setMonth(monthNumber - 1)

    return date.toLocaleString('en-US', { month: 'long' })
  }

  /**
   * Change le scénario pour les séances
   */
  function changeScenarioInput() {
    let q = data.filter((k) => {
      return k.id === parseInt(scenario.value)
    })

    start_time.length = 0

    const event = q[0]['start_time']

    event.forEach((v) => {
      const newOption = document.createElement('option')
      const optionText = document.createTextNode(v.start_time)
      newOption.appendChild(optionText)
      newOption.setAttribute('value', v.id)
      start_time.appendChild(newOption)
    })

    participant.value = q[0]['min_participant']
    participant.setAttribute('min', q[0]['min_participant'])
    participant.setAttribute('max', q[0]['max_participant'])

    price.setAttribute('value', q[0]['min_participant'] * q[0]['price'])
  }

  /**
   * Change le nombre de participants
   */
  function changeParticipantInput() {
    let q = data.filter((k) => {
      return k.id === parseInt(scenario.value)
    })

    price.setAttribute('value', parseInt(participant.value) * q[0]['price'])
  }

  /**
   * définit le message de notification
   * @param classToRemove
   * @param classToAdd
   * @param html
   */
  function setNotificationMessage(classToRemove, classToAdd, html) {
      notificationMsg.classList.remove(classToRemove)
      notificationMsg.classList.add(classToAdd)
      notificationMsg.innerHTML = html
  }

  /**
   * Retourne une url
   * @param day
   * @param nav
   * @param path
   * @returns {string}
   */
  function getUrl(day, nav, path) {
    let params = {
      day: day,
      nav: nav,
      scenario: path,
    }

    let url = baseUrl + 'api/calendar'
    url += '?'
    for (let k in params) {
      url += k + '=' + params[k] + '&'
    }

    return encodeURI(url.slice(0, -1))
  }

  /**
   * Traitements donnés api
   */
  function processData() {
    scenario.length = 0
    data.forEach((v) => {
      const newOption = document.createElement('option')
      const optionText = document.createTextNode(v.title)
      newOption.appendChild(optionText)
      newOption.setAttribute('value', v.id)
      scenario.appendChild(newOption)
    })

    start_time.length = 0

    if (data.length > 0) {
      const event = data[0]['start_time']

      event.forEach((v) => {
        const newOption = document.createElement('option')
        const optionText = document.createTextNode(v.start_time)
        newOption.appendChild(optionText)
        newOption.setAttribute('value', v.id)
        start_time.appendChild(newOption)
      })

      participant.value = data[0]['min_participant']
      participant.setAttribute('min', data[0]['min_participant'])
      participant.setAttribute('max', data[0]['max_participant'])

      price.setAttribute('value', data[0]['min_participant'] * data[0]['price'])
    }
  }

  /**
   * Traitements donnés api
   */
  function processDataWithInterval() {
    data.forEach((v) => {
      let bool = false
      for (let i = 0; i < scenario.length; i++) {
        if (scenario.value === v.id) {
          bool = true
        }
      }
      if (bool) {
        const newOption = document.createElement('option')
        const optionText = document.createTextNode(v.title)
        newOption.appendChild(optionText)
        newOption.setAttribute('value', v.id)
        scenario.appendChild(newOption)
      }
    })

    if (data.length > 0) {
      const event = data[0]['start_time']

      event.forEach((v) => {
        let bool = false
        for (let i = 0; i < start_time.length; i++) {
          if (start_time.value === v.id) {
            bool = true
          }
        }
        if (bool) {
          const newOption = document.createElement('option')
          const optionText = document.createTextNode(v.start_time)
          newOption.appendChild(optionText)
          newOption.setAttribute('value', v.id)
          start_time.appendChild(newOption)
        }
      })

      participant.setAttribute('min', data[0]['min_participant'])
      participant.setAttribute('max', data[0]['max_participant'])
    }
  }

  /**
   * Chargements donnés api
   * @returns {Promise<void>}
   * @param url
   */
  async function loadData(url) {
    await fetch(url)
      .then((response) => response.json())
      .then((result) => {
        data = result['data']

        console.log(data);

        if(!data.length) {
              notificationCard.classList.remove('d-none')
              setNotificationMessage(
                  'alert-info',
                  'alert-danger',
                  'Aucune séance d\'escape game disponible',
              )
              participant.value = 0
              price.setAttribute('value', '0')
        }
        else {
          notificationCard.classList.add('d-none')
        }

        calendar.innerHTML = ''

        calendar.innerHTML = result.content

        const date = result.date.split('-')

        calendar_date.setYear(date[0])
        calendar_date.setMonth(date[1])
        calendar_date.setDay(date[2])

        current_month.textContent = getMonthName(calendar_date.getMonth())

        document.querySelectorAll('td').forEach((td) => {
          td.addEventListener('click', function () {
            let temp_cal = calendar_date
            temp_cal.setDay(td.textContent)
            url = getUrl(temp_cal.getDate(), null, lastPath)
            loadData(url).then(() => {
              processData()
            })
          })
        })
      })
      .catch((error) => {})
  }

  interval_timer = setInterval(function () {
    url = getUrl(calendar_date.getDate(), null, lastPath)
    loadData(url).then((r) => {
      processDataWithInterval()
    })
  }, 5000)

  let calendar_date = new date(new Date())

  url = getUrl(calendar_date.getDate(), null, lastPath)

  current_month.textContent = getMonthName(calendar_date.getMonth())

  loadData(url).then((r) => {
    processData()
  })
})
