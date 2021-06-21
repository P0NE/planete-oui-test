# Planete-oui Test

### Explication

For this test, I chose to use Python because it allows you to quickly create standalone applications.
In addition, python has very practical libraries for data manipulation as requested in this test.
I decided to use Pandas for this.
I use these technologies in my daily work, so I'm more comfortable with it right now.

### Run

I created a docker container to easily launch the application. Just fill in the environment file (provided for simplicity in this case) and build the image.

```sh
docker build -t bcm_test .
```
Then just launch the container with the following command (by correctly entering the arguments)

```sh
docker run --rm --env-file .env.dev bcm_test -f "16-06-2021" -t "17.06.2021" -o "json"
```
