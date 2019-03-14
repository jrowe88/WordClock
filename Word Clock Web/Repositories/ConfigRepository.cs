using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using IniParser;
using IniParser.Model;
using System.Threading.Tasks;


namespace WordClockWeb.Repositories
{    
    public class ConfigRepository
    {        
        private IniData _config;
        FileIniDataParser _parser;

        public ConfigRepository(string filePath)
        {
          FilePath = filePath;
          if (!File.Exists(FilePath))
                throw new InvalidOperationException("File Path does not exist: {FilePath}");

          _parser = new FileIniDataParser();          
          _config = _parser.ReadFile(FilePath);
        }

        public string FilePath { get; private set; }

        public async Task<string> GetValue(string key)        
        {
          return _config["DEFAULT"][key];
        }

        public async void SetValue(string key, string value)
        {
          _config["DEFAULT"][key] = value;
        }

        public void ReadConfig()
        {
          _config = _parser.ReadFile(FilePath);
        }

        public void Save()
        {
          _parser.WriteFile(FilePath, _config);
        }


    }
}