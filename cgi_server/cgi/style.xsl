<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h2>Poems: </h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Poem id</th>
        <th>Poem</th>
        <th>Email</th>
      </tr>
      <xsl:for-each select="poem">
        <tr>
          <td><xsl:value-of select="poemfield[@navn='poemId']"/></td>
          <td><xsl:value-of select="poemfield[@navn='poem']"/></td>
          <td><xsl:value-of select="poemfield[@navn='email']"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
