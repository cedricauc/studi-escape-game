class date {
    constructor(now) {
        this.year = now.getFullYear()
        this.month = now.getMonth() + 1
        this.day = now.getDate()
    }

    getYear() {
        return this.year
    }

    setYear(year) {
        this.year = year
    }

    getMonth() {
        return this.month
    }

    setMonth(month) {
        this.month = month
    }

    getDay(day) {
        return this.day
    }

    setDay(day) {
        this.day = day
    }

    getDate() {
        return this.getYear() + '-' + this.getMonth() + '-' + this.getDay()
    }
}
