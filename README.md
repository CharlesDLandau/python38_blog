# Python38_Tour

This is the source repo for this blog, and it also includes a Dockerfile for simply launching python 3.8 without having to install it locally. So:

```bash
//build
docker build -t <img_tag> .

//run on *nix
docker run -p 8888:8888 -it --rm -v $(PWD):/code --name dev <img_tag>

//run on windows
docker run -p 8888:8888 -it --rm -v %CD%:/code --name dev <img_tag>
```

If all goes well you'll be prompted to copy a URL into your browser, which will point to your local port 8888 with a token to authorize access to the Jupyter instance.