module Jekyll
  module UnbraceFilter
    def unbrace(input)
      input.to_s.delete("{}")
    end
  end
end

Liquid::Template.register_filter(Jekyll::UnbraceFilter)
