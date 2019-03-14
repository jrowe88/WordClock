using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using WordClockWeb.Repositories;

namespace WordClockWeb.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ConfigController : Controller
    {

      private readonly ConfigRepository _repository;

      public ConfigController(ConfigRepository repository)
      {
          _repository = repository;
      }

      [HttpGet("{key}")]
      [ProducesResponseType(StatusCodes.Status404NotFound)]
      public async Task<ActionResult<KeyValuePair<string,string>>> GetValueAsync(string key)
      {
          string value = await _repository.GetValue(key);
          if (value != null)
              return new KeyValuePair<string, string>(key, value);
          return NotFound(key);

      }

      [HttpGet]
      [ProducesResponseType(StatusCodes.Status404NotFound)]
      public async Task<ActionResult<KeyValuePair<string,string>>> GetConfigPath()
      {
          return new KeyValuePair<string, string>("configPath", _repository.FilePath);
      }


      [HttpPut]
      [ProducesResponseType(StatusCodes.Status201Created)]
      [ProducesResponseType(StatusCodes.Status400BadRequest)]
      public async Task<ActionResult<KeyValuePair<string,string>>> CreateValueAsync(KeyValuePair<string,string> kvp)
      {
          if (!ModelState.IsValid)
          {
              return BadRequest(ModelState);
          }

          _repository.SetValue(kvp.Key, kvp.Value);
          _repository.Save();

          return CreatedAtAction(nameof(CreateValueAsync), kvp);
      }

    }
}

