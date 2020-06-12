# HFAPIv2
A Python wrapper for the HF API v2

## Usage

Simple usage example:

```python
bot = HF_API()
bot.set_client_id("client-secret");
bot.set_secret_key("secret-key");

print(f"Authorization URL: {bot.gen_auth_url()}")
```

This will return to your oAuth redirect url with a token.

You can further interact with HF like so:
```python
bot = HF_API()
bot.set_client_id("client-secret-value");
bot.set_secret_key("secret-key-value");
bot.set_access_token("access-token-value");

# Look up a users byte history
foo = bot.action("read",{
    "bytes": {
        "_uid": 1341148,
        "amount": True,
        "dateline": True,
        "type": True,
        "reason": True
    }
})

print(foo)

# write a post the easy way:
bot.write_post(self, 6083735, "This is a test post using the HFAPI v2")

# write a post the 'hard' way:
bot.action("write", {
  "posts": {
    "_tid": 6083735,
    "_message": "This is a test post using the HFAPI v2"
  }
})
```
## Further Reading

See the official HF API Forum for more information
https://hackforums.net/forumdisplay.php?fid=375
