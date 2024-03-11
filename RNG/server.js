const express = require('express')
const app = express()
const port = 5555

app.get('/', (req, res) => {
	res.send('random number generator')
})

app.get('/random', (req, res) => {
	const randomNum = Math.floor(Math.random() * 10000)
	res.json({random: randomNum})
})

app.listen(port, () => {
	console.log(`RNG running on port ${port}`)
})